
from openai import OpenAI
from pinecone import Pinecone

from config import *

# Initialize OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)


def ask_question(question):

    # 1. Convert question into embedding
    embedding = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=question
    ).data[0].embedding

    # 2. Search similar content in Pinecone
    results = index.query(
        vector=embedding,
        top_k=4,
        include_metadata=True,
        namespace=NAMESPACE
    )

    # 3. Collect relevant PDF content
    context = ""

    for match in results.matches:

        if match.metadata and match.metadata.get("text"):
            context += match.metadata["text"] + "\n\n"

    # 4. Check whether context is available
    if not context:
        return "Sorry, I couldn't find the answer in the documents."

    # 5. Send context and question to OpenAI
    response = client.responses.create(
        model=CHAT_MODEL,
        instructions="""
        You are a helpful customer support assistant.
        Answer questions using only the given context.
        If information is not available, say you don't know.
        Do not invent any information.
        """,
        input=f"""
        Context:
        {context}

        Question:
        {question}

        Answer:
        """
    )

    return response.output_text


# Test chatbot
if __name__ == "__main__":

    while True:

        question = input("\nAsk your question (type exit to stop): ")

        if question.lower() == "exit":
            break

        answer = ask_question(question)

        print("\nChatbot:", answer)
