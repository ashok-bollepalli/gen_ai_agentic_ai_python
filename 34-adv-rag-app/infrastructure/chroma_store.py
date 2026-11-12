import chromadb
from infrastructure.config import CHROMA_FOLDER, COLLECTION_NAME

# Persistent ChromaDB: data remains on disk between application runs.
client = chromadb.PersistentClient(path=CHROMA_FOLDER)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)

def add_chunks(chunks, embeddings):
    """Save text, metadata and embeddings in ChromaDB."""
    if not chunks:
        return

    collection.add(
        ids=[chunk["chunk_id"] for chunk in chunks],
        documents=[chunk["text"] for chunk in chunks],
        metadatas=[chunk["metadata"] for chunk in chunks],
        embeddings=embeddings
    )

def search_vectors(query_embedding, top_k=10):
    """Find similar chunks using vector similarity."""
    if collection.count() == 0:
        return []

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count())
    )

    chunks = []
    for i, chunk_id in enumerate(result["ids"][0]):
        chunks.append({
            "chunk_id": chunk_id,
            "text": result["documents"][0][i],
            "metadata": result["metadatas"][0][i],
            "vector_distance": result["distances"][0][i]
        })

    return chunks

def get_chunk_count():
    return collection.count()

def clear_database():
    """Remove old records before rebuilding the knowledge base."""
    global collection
    client.delete_collection(COLLECTION_NAME)
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )
