import json
from openai import OpenAI

from src.config import OPENAI_API_KEY, CHAT_MODEL
from src.vector_store.chroma_store import search_documents

client = OpenAI(api_key=OPENAI_API_KEY)


# 1. Call OpenAI LLM
def ask_llm(prompt):
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()


# 2. Check whether retrieved documents are relevant
def check_relevance(question, documents):
    if not documents:
        return False

    context = "\n".join(doc["text"] for doc in documents)

    prompt = f"""
    Check whether the CONTEXT can answer the QUESTION.

    Return only JSON:
    {{"relevant": true}} or {{"relevant": false}}

    QUESTION: {question}

    CONTEXT: {context}
    """

    result = ask_llm(prompt)

    try:
        result = json.loads(result)
        return result["relevant"]
    except:
        return False


# 3. Rewrite question if retrieval is not relevant
def rewrite_question(question):
    prompt = f"""
    Rewrite this question into a better search query.
    Keep the original meaning.
    Question: {question}
    """
    return ask_llm(prompt)


# 4. Generate final answer
def generate_answer(question, documents):
    context = "\n".join(
        doc["text"] for doc in documents
    )

    prompt = f"""
    You are a customer support assistant.

    Answer the question using ONLY the given context.
    Do not make up information.
    If the answer is unavailable, say you don't know.

    QUESTION:
    {question}

    CONTEXT:
    {context}
    """
    return ask_llm(prompt)


# 5. Main Corrective RAG function
def answer_customer_question(question, collection):
    # First retrieval
    documents = search_documents(question, collection)

    # Check relevance
    if not check_relevance(question, documents):
        # Rewrite question
        new_question = rewrite_question(question)
        # Second retrieval
        documents = search_documents(new_question, collection)

    # Final relevance check
    if check_relevance(question, documents):
        answer = generate_answer(question, documents)
        return answer
    return "Sorry, I couldn't find the answer in the available documents."