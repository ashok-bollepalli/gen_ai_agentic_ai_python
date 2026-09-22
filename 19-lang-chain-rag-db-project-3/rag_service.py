from pathlib import Path

from pinecone import Pinecone, ServerlessSpec

from langchain_openai import OpenAIEmbeddings

from langchain_pinecone import PineconeVectorStore

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_core.documents import Document

from config import (
    OPENAI_EMBEDDING_MODEL,
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME,
    PINECONE_NAMESPACE
)


def create_index():

    pc = Pinecone(
        api_key=PINECONE_API_KEY
    )

    indexes = [
        index["name"]
        for index in pc.list_indexes()
    ]

    if PINECONE_INDEX_NAME not in indexes:

        pc.create_index(
            name=PINECONE_INDEX_NAME,

            dimension=1536,

            metric="cosine",

            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )

        print("Pinecone index created.")

    else:

        print("Pinecone index already exists.")


def load_documents():

    documents = []

    folder = Path("documents")

    for file in folder.glob("*.txt"):

        text = file.read_text(
            encoding="utf-8"
        )

        documents.append(
            Document(
                page_content=text,

                metadata={
                    "source": file.name
                }
            )
        )

    return documents


def get_vector_store():

    embeddings = OpenAIEmbeddings(
        model=OPENAI_EMBEDDING_MODEL
    )

    vector_store = PineconeVectorStore(
        index_name=PINECONE_INDEX_NAME,

        embedding=embeddings,

        namespace=PINECONE_NAMESPACE
    )

    return vector_store


def ingest_documents():

    create_index()

    documents = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(
        documents
    )

    print(
        f"Documents: {len(documents)}"
    )

    print(
        f"Chunks: {len(chunks)}"
    )

    vector_store = get_vector_store()

    vector_store.add_documents(
        chunks
    )

    print(
        "Documents added to Pinecone."
    )


def retrieve_documents(question):

    vector_store = get_vector_store()

    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": 4
        }
    )

    documents = retriever.invoke(
        question
    )

    return documents


if __name__ == "__main__":

    ingest_documents()
