"""Script to index company policy documents into local FAISS."""

import logging
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.rag.embeddings import document_processor
from app.rag.indexer import indexer
from app.config import setup_logging, settings

# Setup logging
setup_logging(settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


def main():
    """Index all PDF documents in the documents directory."""
    logger.info("=" * 60)
    logger.info("Document Indexing Script")
    logger.info("=" * 60)

    # Path to documents
    documents_dir = Path(__file__).parent.parent / "documents"

    if not documents_dir.exists():
        logger.error(f"Documents directory not found: {documents_dir}")
        return 1

    try:
        # Step 1: Reset existing index for clean rebuild
        logger.info("\nStep 1: Resetting existing FAISS index (if any)...")
        indexer.delete_index()
        logger.info("✓ Previous index cleared")

        # Step 2: Create or update the local index
        logger.info("\nStep 2: Creating/updating local FAISS index...")
        indexer.create_index()
        logger.info("✓ Index ready")

        # Step 3: Process all PDF documents
        logger.info("\nStep 3: Processing PDF documents...")
        chunks = document_processor.process_all_documents(documents_dir)

        if not chunks:
            logger.error("No documents were processed!")
            return 1

        logger.info(f"✓ Processed {len(chunks)} total chunks")

        # Step 4: Upload to local FAISS
        logger.info("\nStep 4: Uploading documents to FAISS...")
        indexer.upload_documents(chunks)
        logger.info("✓ Documents uploaded")

        # Step 5: Verify
        logger.info("\nStep 5: Verifying indexing...")
        doc_count = indexer.get_document_count()
        logger.info(f"✓ Index contains {doc_count} documents")

        logger.info("\n" + "=" * 60)
        logger.info("✓ Indexing completed successfully!")
        logger.info("=" * 60)

        return 0

    except Exception as e:
        logger.error(f"\n✗ Indexing failed: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
