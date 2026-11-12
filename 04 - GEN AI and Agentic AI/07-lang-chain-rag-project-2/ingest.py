from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from pinecone import Pinecone, ServerlessSpec

from config import (
    OPENAI_API_KEY,
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME,
    EMBEDDING_MODEL
)


# =====================================================
# 1. INITIALIZE PINECONE
# =====================================================

pc = Pinecone(
    api_key=PINECONE_API_KEY
)


# =====================================================
# 2. CREATE INDEX IF NOT AVAILABLE
# =====================================================

existing_indexes = [
    index["name"]
    for index in pc.list_indexes()
]


if PINECONE_INDEX_NAME not in existing_indexes:

    print(
        f"Index '{PINECONE_INDEX_NAME}' not found."
    )

    print(
        f"Creating index '{PINECONE_INDEX_NAME}'..."
    )

    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

    print("Index created successfully.")

else:

    print(
        f"Index '{PINECONE_INDEX_NAME}' already exists."
    )


# =====================================================
# 3. LOAD PDF
# =====================================================

loader = PyPDFLoader(
    "documents/gen_ai_notes.pdf"
)

documents = loader.load()

print(
    "Total pages:",
    len(documents)
)


# =====================================================
# 4. SPLIT DOCUMENT
# =====================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(
    documents
)

print(
    "Total chunks:",
    len(chunks)
)


# =====================================================
# 5. CREATE EMBEDDINGS
# =====================================================

embeddings = OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
    api_key=OPENAI_API_KEY
)


# =====================================================
# 6. STORE DOCUMENTS IN PINECONE
# =====================================================

vector_store = PineconeVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    index_name=PINECONE_INDEX_NAME
)


print(
    "Documents successfully stored in Pinecone."
)