"""Local FAISS index management and document uploading."""

import logging
import shutil
from pathlib import Path
from typing import Any, Dict, List

try:
    from langchain_core.documents import Document
except ImportError:  # pragma: no cover - compatibility fallback
    from langchain.schema import Document

try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:  # pragma: no cover - compatibility fallback
    from langchain_community.embeddings import HuggingFaceEmbeddings

try:
    from langchain_community.vectorstores import FAISS
except ImportError:  # pragma: no cover - compatibility fallback
    from langchain.vectorstores import FAISS

from app.config import settings

logger = logging.getLogger(__name__)


class FaissIndexer:
    """Manage local FAISS index and document uploads."""

    def __init__(self):
        """Initialize FAISS index components."""
        self.index_path = Path(settings.FAISS_INDEX_PATH)
        self.embeddings = None
        self.vectorstore = None

        logger.info("FaissIndexer initialized")

    def _get_embeddings(self):
        """Lazily initialize embedding model to reduce startup fragility."""
        if self.embeddings is None:
            self.embeddings = HuggingFaceEmbeddings(
                model_name=settings.EMBEDDING_MODEL_NAME,
            )
        return self.embeddings

    def create_index(self) -> None:
        """Create local FAISS index directory if needed."""
        self.index_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"FAISS index directory ready: {self.index_path}")

    def upload_documents(self, documents: List[Dict[str, Any]]) -> None:
        """
        Upload documents to the local FAISS index.

        Args:
            documents: List of document dictionaries with embeddings
        """
        if not documents:
            logger.warning("No documents to upload")
            return

        logger.info(f"Uploading {len(documents)} documents to FAISS index")

        try:
            faiss_docs = []
            seen_ids = set()
            for doc in documents:
                doc_id = str(doc.get('id', '')).strip()
                content = str(doc.get('content', '')).strip()
                if not doc_id or not content:
                    continue
                if doc_id in seen_ids:
                    continue
                seen_ids.add(doc_id)

                metadata = dict(doc.get('metadata', {}))
                metadata['id'] = doc_id
                faiss_docs.append(
                    Document(page_content=content, metadata=metadata)
                )

            if not faiss_docs:
                logger.warning("No valid documents found after validation")
                return

            existing = self._load_vectorstore()
            if existing:
                existing.add_documents(faiss_docs)
                self.vectorstore = existing
            else:
                self.vectorstore = FAISS.from_documents(faiss_docs, self._get_embeddings())

            self.vectorstore.save_local(str(self.index_path))
            logger.info("All documents uploaded successfully to FAISS [valid=%s]", len(faiss_docs))

        except Exception as e:
            logger.error(f"Error uploading documents: {str(e)}")
            raise

    def delete_index(self) -> None:
        """Delete the local FAISS index."""
        logger.info(f"Deleting FAISS index at: {self.index_path}")
        if self.index_path.exists():
            shutil.rmtree(self.index_path)
            logger.info("FAISS index deleted successfully")

    def get_document_count(self) -> int:
        """
        Get the number of documents in the FAISS index.

        Returns:
            Document count
        """
        try:
            vectorstore = self._load_vectorstore()
            if not vectorstore:
                return 0

            count = len(vectorstore.index_to_docstore_id)
            logger.info(f"FAISS index contains {count} documents")
            return count

        except Exception as e:
            logger.error(f"Error getting FAISS document count: {str(e)}")
            return 0

    def _load_vectorstore(self):
        """Load the FAISS store from disk if it exists."""
        if self.vectorstore is not None:
            return self.vectorstore

        index_file = self.index_path / "index.faiss"
        store_file = self.index_path / "index.pkl"
        if not (index_file.exists() and store_file.exists()):
            return None

        self.vectorstore = FAISS.load_local(
            str(self.index_path),
            self._get_embeddings(),
            allow_dangerous_deserialization=True,
        )
        return self.vectorstore


# Global indexer instance
indexer = FaissIndexer()
