"""
RAG = Retrieval Augmented Generation.

1. Read bank policy documents (knowledge_base/*.md)
2. Split into small chunks
3. Convert chunks to vectors (OpenAI embeddings)
4. Store in Chroma vector DB
5. At question time -> find the most similar chunks
"""
from functools import lru_cache
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import get_settings

COLLECTION = "bank_policies"


def _load_documents(folder: str) -> list[Document]:
    docs = []
    for file in sorted(Path(folder).glob("*.md")):
        docs.append(Document(page_content=file.read_text(encoding="utf-8"),
                             metadata={"source": file.name}))
    return docs


@lru_cache
def get_vector_store() -> Chroma:
    settings = get_settings()
    store = Chroma(
        collection_name=COLLECTION,
        embedding_function=OpenAIEmbeddings(model=settings.openai_embedding_model,
                                            api_key=settings.openai_api_key),
        persist_directory=settings.chroma_dir,
    )
    # Build the index only once (first start)
    if not store.get(limit=1)["ids"]:
        ingest(store)
    return store


def ingest(store: Chroma) -> int:
    settings = get_settings()
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(_load_documents(settings.knowledge_base_dir))
    store.add_documents(chunks)
    print(f"[RAG] Indexed {len(chunks)} chunks into Chroma")
    return len(chunks)


def search_policies(question: str, k: int = 4) -> str:
    """Return the top-k matching chunks as one text block (with source names)."""
    results = get_vector_store().similarity_search(question, k=k)
    return "\n\n".join(f"[{d.metadata['source']}]\n{d.page_content}" for d in results)
