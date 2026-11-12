from infrastructure.document_loader import load_documents
from application.chunking import create_chunks
from infrastructure.openai_service import create_embeddings
from infrastructure.chroma_store import add_chunks, clear_database

def ingest_documents():
    """Complete document ingestion workflow."""
    documents = load_documents()
    chunks = create_chunks(documents)

    # Generate embeddings once during ingestion.
    texts = [chunk["text"] for chunk in chunks]
    embeddings = create_embeddings(texts)

    # Save vectors, text and metadata in persistent ChromaDB.
    clear_database()
    add_chunks(chunks, embeddings)

    return len(chunks)
