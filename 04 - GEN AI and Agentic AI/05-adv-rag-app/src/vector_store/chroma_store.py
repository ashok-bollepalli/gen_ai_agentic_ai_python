import chromadb
from openai import OpenAI
from src.config import OPENAI_API_KEY, EMBEDDING_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)
chroma_client = chromadb.PersistentClient(path="chroma_db")
COLLECTION_NAME = "customer_documents"

def get_embeddings(texts):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts
    )
    return [item.embedding for item in response.data]

def create_vector_store(chunks):
    """Create or replace the Chroma collection with PDF chunks."""
    try:
        chroma_client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = chroma_client.create_collection(COLLECTION_NAME)

    for start in range(0, len(chunks), 50):
        batch = chunks[start:start + 50]
        texts = [item["text"] for item in batch]
        embeddings = get_embeddings(texts)
        ids = [f"chunk-{start + i}" for i in range(len(batch))]
        metadatas = [
            {"source": item["source"], "page": item["page"]}
            for item in batch
        ]

        collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas
        )

    return collection

def search_documents(question, collection, top_k=4):
    query_embedding = get_embeddings([question])[0]
    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = result["documents"][0] if result["documents"] else []
    metadatas = result["metadatas"][0] if result["metadatas"] else []

    return [
        {"text": doc, "source": meta["source"], "page": meta["page"]}
        for doc, meta in zip(documents, metadatas)
    ]
