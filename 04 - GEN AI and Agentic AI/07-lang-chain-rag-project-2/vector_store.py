from langchain_pinecone import PineconeVectorStore

from config import PINECONE_INDEX_NAME

from llm import embeddings


# =====================================================
# PINECONE VECTOR STORE
# =====================================================

vector_store = PineconeVectorStore(
    index_name=PINECONE_INDEX_NAME,
    embedding=embeddings
)


# =====================================================
# RETRIEVER
# =====================================================

retriever = vector_store.as_retriever(
    search_kwargs={
        "k": 4
    }
)