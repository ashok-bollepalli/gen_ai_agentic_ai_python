import os

import chromadb

from dotenv import load_dotenv
from openai import OpenAI

# load env variables
load_dotenv()

# get api key
api_key = os.getenv("OPENAI_API_KEY")

# Create OpenAI Client
client = OpenAI(api_key=api_key)

# Create Persistent ChromaDB Client
chroma_client = chromadb.PersistentClient(path ="./chroma_db")

# Create or get collection
collection = chroma_client.get_or_create_collection(name="company_documents")

# read document
with open("documents/company.txt", "r", encoding="utf-8") as file:
    document = file.read()

    # split document into chunks
    chunks = document.split("\n\n")

    #Generate embeddings and store them

    for index, chunk in enumerate(chunks):
        response = client.embeddings.create(
            model = "text-embedding-3-small",
            input = chunk,
        )

        embedding = response.data[0].embedding

        collection.add(
            ids =[f"chunk-{index}"],
            documents = [chunk],
            embeddings = embedding
        )

print("Document successfully stored in ChromaDB.")