"""
RAG layer: bank policy documents -> chunks -> embeddings -> Chroma vector DB.

Run once to build the index:   python -m app.rag.vector_store
"""
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from app.config import POLICY_DIR, CHROMA_DIR, EMBEDDING_MODEL

COLLECTION = "bank_policies"


def _embeddings():
    return OpenAIEmbeddings(model=EMBEDDING_MODEL)


def build_index() -> int:
    """Load -> Split -> Embed -> Store. Returns number of chunks stored."""
    # 1. Load all markdown policy files
    docs = DirectoryLoader(str(POLICY_DIR), glob="*.md", loader_cls=TextLoader).load()

    # 2. Split into small overlapping chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    # 3 + 4. Embed and save into Chroma (stored on disk in chroma_db/)
    store = get_store()
    store.reset_collection()  # avoid duplicates when re-running
    store.add_documents(chunks)
    return len(chunks)


def get_store() -> Chroma:
    return Chroma(collection_name=COLLECTION, embedding_function=_embeddings(),
                  persist_directory=str(CHROMA_DIR))


def search_policies(question: str, k: int = 3) -> str:
    """Return the top-k matching chunks as one text block (with source file names)."""
    results = get_store().similarity_search(question, k=k)
    return "\n\n".join(
        f"[Source: {d.metadata.get('source', '').split('/')[-1]}]\n{d.page_content}"
        for d in results
    )


if __name__ == "__main__":
    print(f"✅ Indexed {build_index()} chunks into Chroma at {CHROMA_DIR}")
