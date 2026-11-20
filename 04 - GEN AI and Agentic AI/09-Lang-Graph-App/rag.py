
import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

# 1. Create Embeddings
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

# 2. Create Vector Database
vector_db = Chroma(
    collection_name="banking_policies",
    persist_directory="./chroma_db",
    embedding_function=embeddings
)


# 3. Data Ingestion
def ingest_policy_documents():

    # Load policy document
    loader = TextLoader("policies/banking_policy.txt")

    documents = loader.load()

    # Split document into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    # Store chunks in ChromaDB
    vector_db.add_documents(chunks)

    print("Policy documents successfully ingested!")


# 4. Search Policy
def search_policy(question):

    documents = vector_db.similarity_search(
        question,
        k=3
    )

    result = ""

    for doc in documents:
        result += doc.page_content + "\n"

    return result
