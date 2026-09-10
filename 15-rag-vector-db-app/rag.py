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

def ask_question(question):

    # create embedding for the question
    response = client.embeddings.create(
        model = "text-embedding-3-small",
        input = question
    )

    question_embedding = response.data[0].embedding

    # search chroma DB
    results = collection.query(
        query_embeddings = question_embedding,
        n_results = 3
    )

    print("Results:", results)

    # Get Retrieved Documents
    documents = results["documents"][0]

    print("documents:", documents)

    #combine documents into context
    context = "\n\n".join(documents)

    print("Context:", context)

    # Create RAG Prompt
    prompt = f"""
    
    Answer the question using only the context provided below.
    
    Context : {context}
    
    Question : {question}

"""

    response = client.responses.create(
        model = "gpt-6-astra",
        input = prompt
    )

    return response.output_text

# simple test to run
if __name__ == "__main__":
    question = input("Ask a question:")
    answer = ask_question(question)

    print(answer)
