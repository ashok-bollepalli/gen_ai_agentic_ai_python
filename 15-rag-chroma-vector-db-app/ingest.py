import os

import chromadb

from dotenv import load_dotenv
from openai import OpenAI

# load env props
load_dotenv()

# get openai api key
apikey  = os.getenv("OPENAI_API_KEY")

# get open ai embedding model
embedding_model = os.getenv("EMBEDDING_MODEL")

# create OpenAI api client
client = OpenAI(api_key=apikey)

# create Chroma DB Client
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# create or get collection
collection = chroma_client.get_or_create_collection(name="company_documents")

# read document
# split into chunks
# generate embeddings
# store embeddings into chroma collection

with open("documents/company.txt", "r") as file:
    data = file.read()

    chunks = data.split("\n")

    #print(chunks)

    for index, chunk in enumerate(chunks):

        # convert each chunk into embdding
        response = client.embeddings.create(
            model = embedding_model,
            input = chunk
        )

        embedding = response.data[0].embedding

        collection.add(
            ids = [f"chunk_{index}"],
            documents = [chunk],
            embeddings=embedding
        )

print("Document successfully stored in ChromaDB.")


