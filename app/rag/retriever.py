"""Document retrieval using local FAISS vector search."""

import logging
from pathlib import Path
from typing import Any, Dict, List

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from app.config import settings

logger = logging.getLogger(__name__)


class DocumentRetriever:
    """Retrieve relevant documents using local FAISS similarity search."""

    def __init__(self):
        """Initialize document retriever."""
        self.index_path = Path(settings.FAISS_INDEX_PATH)
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL_NAME,
        )
        self.vectorstore = None

        logger.info("DocumentRetriever initialized")

    def retrieve(
        self,
        query: str,
        top_k: int = None,
        relevance_threshold: float = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query.

        Args:
            query: Search query string
            top_k: Number of documents to retrieve (default from settings)
            relevance_threshold: Minimum relevance score (default from settings)

        Returns:
            List of relevant documents with metadata and scores
        """
        top_k = top_k or settings.RAG_TOP_K
        relevance_threshold = relevance_threshold or settings.RAG_RELEVANCE_THRESHOLD

        logger.info(f"Retrieving documents for query: '{query}' (top_k={top_k})")

        try:
            vectorstore = self._load_vectorstore()
            if not vectorstore:
                logger.warning("No FAISS index found. Run document indexing first.")
                return []

            # Over-fetch and then filter for better precision/diversity.
            raw_results = vectorstore.similarity_search_with_score(query, k=max(top_k * 3, top_k))

            # Process, deduplicate, and limit per document.
            documents = []
            seen_keys = set()
            doc_counts: Dict[str, int] = {}
            per_document_cap = 2

            for doc, distance in raw_results:
                score = 1.0 / (1.0 + float(distance))

                # Filter by relevance threshold
                if score < relevance_threshold:
                    logger.debug(
                        f"Skipping result with score {score:.3f} "
                        f"(threshold: {relevance_threshold})"
                    )
                    continue

                doc_name = doc.metadata.get('document', 'unknown')
                page = doc.metadata.get('page')
                chunk_index = doc.metadata.get('chunk_index', 0)
                dedup_key = (doc_name, page, chunk_index)

                if dedup_key in seen_keys:
                    continue

                if doc_counts.get(doc_name, 0) >= per_document_cap:
                    continue

                seen_keys.add(dedup_key)
                doc_counts[doc_name] = doc_counts.get(doc_name, 0) + 1

                doc = {
                    'content': doc.page_content,
                    'document': doc_name,
                    'source_path': doc.metadata.get('source_path', ''),
                    'chunk_index': chunk_index,
                    'page': page,
                    'relevance_score': float(score),
                }
                documents.append(doc)

                if len(documents) >= top_k:
                    break

            logger.info(
                f"Retrieved {len(documents)} relevant documents "
                f"(threshold: {relevance_threshold})"
            )

            return documents

        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            raise

    def _load_vectorstore(self):
        """Load FAISS store from disk if available."""
        if self.vectorstore is not None:
            return self.vectorstore

        index_file = self.index_path / "index.faiss"
        store_file = self.index_path / "index.pkl"
        if not (index_file.exists() and store_file.exists()):
            return None

        self.vectorstore = FAISS.load_local(
            str(self.index_path),
            self.embeddings,
            allow_dangerous_deserialization=True,
        )
        return self.vectorstore

    def format_context(self, documents: List[Dict[str, Any]]) -> str:
        """
        Format retrieved documents into context string for LLM.

        Args:
            documents: List of retrieved documents

        Returns:
            Formatted context string
        """
        if not documents:
            return "No relevant documents found."

        context_parts = []
        for i, doc in enumerate(documents, 1):
            page_label = f", Page {doc['page']}" if doc.get('page') else ""
            context_parts.append(
                f"[Source {i}: {doc['document']}{page_label}]\n"
                f"{doc['content']}\n"
            )

        context = "\n---\n".join(context_parts)
        return context

    def get_sources_summary(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Create a summary of source documents.

        Args:
            documents: List of retrieved documents

        Returns:
            List of source summaries for response
        """
        if not documents:
            return []

        # Group by document and keep best score with best page/snippet.
        doc_scores: Dict[str, Dict[str, Any]] = {}
        for doc in documents:
            doc_name = doc['document']
            score = doc['relevance_score']

            if doc_name not in doc_scores or score > doc_scores[doc_name]['score']:
                doc_scores[doc_name] = {
                    'score': score,
                    'page': doc.get('page'),
                    'snippet': self._get_snippet(documents, doc_name),
                }

        # Create source summaries
        sources = [
            {
                'document': doc_name,
                'page': details.get('page'),
                'relevance_score': round(details['score'], 2),
                'snippet': details['snippet']
            }
            for doc_name, details in sorted(
                doc_scores.items(),
                key=lambda x: x[1]['score'],
                reverse=True
            )
        ]

        return sources

    def _get_snippet(self, documents: List[Dict[str, Any]], doc_name: str) -> str:
        """
        Get a short snippet from a document.

        Args:
            documents: All retrieved documents
            doc_name: Document name to get snippet from

        Returns:
            Short snippet (first 150 chars)
        """
        for doc in documents:
            if doc['document'] == doc_name:
                content = doc['content']
                snippet = content[:150]
                if len(content) > 150:
                    snippet += "..."
                return snippet
        return ""


# Global retriever instance
retriever = DocumentRetriever()
