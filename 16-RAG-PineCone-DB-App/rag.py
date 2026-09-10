import os

from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone


# ============================================================
# Load environment variables
# ============================================================

load_dotenv()


# ============================================================
# Get API keys
# ============================================================

openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")


# ============================================================
# Create OpenAI Client
# ============================================================

client = OpenAI(api_key=openai_api_key)


# ============================================================
# Create Pinecone Client
# ============================================================

pc = Pinecone(api_key=pinecone_api_key)


# ============================================================
# Connect to Pinecone Index
# ============================================================

index = pc.Index("company-documents")


# ============================================================
# Ask Question Function
# ============================================================

def ask_question(question):

    # --------------------------------------------------------
    # Create embedding for the question
    # --------------------------------------------------------

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    )

    question_embedding = response.data[0].embedding


    # --------------------------------------------------------
    # Search Pinecone
    # --------------------------------------------------------

    results = index.query(
        vector=question_embedding,
        top_k=3,
        include_metadata=True
    )

    print("Results:", results)


    # --------------------------------------------------------
    # Get Retrieved Documents
    # --------------------------------------------------------

    documents = []

    for match in results["matches"]:

        document = match["metadata"]["text"]

        documents.append(document)


    print("Documents:", documents)


    # --------------------------------------------------------
    # Combine Documents into Context
    # --------------------------------------------------------

    context = "\n\n".join(documents)

    print("Context:", context)


    # --------------------------------------------------------
    # Create RAG Prompt
    # --------------------------------------------------------

    prompt = f"""

    Answer the question using only the context provided below.

    Context:
    {context}

    Question:
    {question}

    """


    # --------------------------------------------------------
    # Send Prompt to GPT
    # --------------------------------------------------------

    response = client.responses.create(
        model="gpt-6-astra",
        input=prompt
    )


    # --------------------------------------------------------
    # Return Answer
    # --------------------------------------------------------

    return response.output_text


# ============================================================
# Simple Test to Run
# ============================================================

if __name__ == "__main__":

    question = input("Ask a question: ")

    answer = ask_question(question)

    print("\nAnswer:")
    print(answer)