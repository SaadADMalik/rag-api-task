"""Document processing and embedding generation for RAG."""

import logging
import hashlib
from pathlib import Path
from typing import Any, Dict, List

from PyPDF2 import PdfReader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Process PDF documents into chunks with embeddings."""

    def __init__(self):
        """Initialize document processor."""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.RAG_CHUNK_SIZE,
            chunk_overlap=settings.RAG_CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL_NAME,
        )

        logger.info("DocumentProcessor initialized")

    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """
        Extract text from a PDF file.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Extracted text content
        """
        try:
            reader = PdfReader(str(pdf_path))
            text = ""

            for page_num, page in enumerate(reader.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text += f"\n--- Page {page_num} ---\n{page_text}"

            logger.info(f"Extracted {len(text)} characters from {pdf_path.name}")
            return text

        except Exception as e:
            logger.error(f"Error extracting text from {pdf_path}: {str(e)}")
            raise

    def chunk_text(self, text: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Split text into chunks with metadata.

        Args:
            text: Text content to chunk
            metadata: Metadata to attach to chunks

        Returns:
            List of chunk dictionaries with text and metadata
        """
        chunks = self.text_splitter.split_text(text)

        chunk_docs = []
        for i, chunk in enumerate(chunks):
            chunk_id = self._generate_chunk_id(
                metadata['document'],
                i,
                chunk
            )

            chunk_docs.append({
                'id': chunk_id,
                'content': chunk,
                'metadata': {
                    **metadata,
                    'chunk_index': i,
                    'total_chunks': len(chunks),
                }
            })

        logger.info(f"Created {len(chunk_docs)} chunks from document")
        return chunk_docs

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.

        Args:
            texts: List of text strings

        Returns:
            List of embedding vectors
        """
        try:
            embeddings = self.embeddings.embed_documents(texts)
            logger.info(f"Generated embeddings for {len(texts)} texts")
            return embeddings

        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise

    def process_document(self, pdf_path: Path) -> List[Dict[str, Any]]:
        """
        Process a single PDF document into chunks with embeddings.

        Args:
            pdf_path: Path to PDF file

        Returns:
            List of processed chunks with embeddings
        """
        logger.info(f"Processing document: {pdf_path.name}")

        # Extract text
        text = self.extract_text_from_pdf(pdf_path)

        # Create metadata
        metadata = {
            'document': pdf_path.name,
            'source_path': str(pdf_path),
        }

        # Chunk text
        chunks = self.chunk_text(text, metadata)

        # Generate embeddings
        texts = [chunk['content'] for chunk in chunks]
        embeddings = self.generate_embeddings(texts)

        # Attach embeddings to chunks
        for chunk, embedding in zip(chunks, embeddings):
            chunk['content_vector'] = embedding

        logger.info(
            f"Document processed: {pdf_path.name} -> "
            f"{len(chunks)} chunks with embeddings"
        )

        return chunks

    def process_all_documents(self, documents_dir: Path) -> List[Dict[str, Any]]:
        """
        Process all PDF documents in a directory.

        Args:
            documents_dir: Path to directory containing PDFs

        Returns:
            List of all processed chunks
        """
        pdf_files = list(documents_dir.glob("*.pdf"))
        logger.info(f"Found {len(pdf_files)} PDF files to process")

        all_chunks = []
        for pdf_path in pdf_files:
            try:
                chunks = self.process_document(pdf_path)
                all_chunks.extend(chunks)
            except Exception as e:
                logger.error(f"Failed to process {pdf_path.name}: {str(e)}")
                continue

        logger.info(
            f"Processed {len(pdf_files)} documents into {len(all_chunks)} total chunks"
        )

        return all_chunks

    @staticmethod
    def _generate_chunk_id(document_name: str, chunk_index: int, content: str) -> str:
        """
        Generate a unique ID for a chunk.

        Args:
            document_name: Name of source document
            chunk_index: Index of chunk in document
            content: Chunk content

        Returns:
            Unique chunk ID
        """
        # Create hash of content for uniqueness
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        return f"{document_name}_{chunk_index}_{content_hash}"


# Global document processor instance
document_processor = DocumentProcessor()
