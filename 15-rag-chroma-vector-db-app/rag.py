import os

import chromadb

from dotenv import load_dotenv
from openai import OpenAI

# load env props
load_dotenv()

# get openai api key
apikey = os.getenv("OPENAI_API_KEY")

# get open ai embedding model
embedding_model = os.getenv("EMBEDDING_MODEL")

# get open ai llm model
llm_model = os.getenv("LLM_MODEL")

# create OpenAI api client
client = OpenAI(api_key=apikey)

# create Chroma DB Client
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# create or get collection
collection = chroma_client.get_or_create_collection(name="company_documents")


def ask_question(question):
    # convert question to embeddings
    response = client.embeddings.create(
        model=embedding_model,
        input=question
    )

    question_embedding = response.data[0].embedding

    # retrieve
    results = collection.query(
        query_embeddings=question_embedding,
        n_results=3
    )

    print("Result : ", results)

    documents = results["documents"][0]

    context = "\n".join(documents)

    print(context)

    # create prompt (augmentation)

    prompt = f"""
    You are a helpful AI assistant for Ashok IT.

    Instructions:
    1. Answer using only the provided context.
    2. Do not use external knowledge.
    3. If the answer is not available in the context,
       respond with "Sorry, I don't have that information."
    4. Provide clear and concise answers.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    # generation
    response = client.responses.create(
        model=llm_model,
        input=prompt
    )

    return response.output_text
