from openai import OpenAI

from src.config import OPENAI_API_KEY, CHAT_MODEL
from src.vector_store.chroma_store import search_documents

client = OpenAI(api_key=OPENAI_API_KEY)


# 1. Call OpenAI
def ask_llm(prompt):
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip()


# 2. Check document relevance
def check_relevance(question, documents):
    context = "\n".join(doc["text"] for doc in documents)

    prompt = f"""
    Are these documents relevant to the question?

    Question: {question}
    Documents: {context}

    Reply only YES or NO.
    """

    return ask_llm(prompt).upper().startswith("YES")


# 3. Generate answer
def generate_answer(question, documents):
    context = "\n".join(doc["text"] for doc in documents)

    prompt = f"""
    Answer the customer question using only the documents.

    Question: {question}

    Documents:
    {context}

    Do not invent information.
    """

    return ask_llm(prompt)


# 4. Check whether answer is supported by documents
def check_support(answer, documents):
    context = "\n".join(doc["text"] for doc in documents)

    prompt = f"""
    Is the answer completely supported by the documents?

    Documents:
    {context}

    Answer:
    {answer}

    Reply only YES or NO.
    """

    return ask_llm(prompt).upper().startswith("YES")


# 5. Check whether answer addresses the question
def check_answer(question, answer):
    prompt = f"""
    Does this answer correctly address the question?

    Question: {question}

    Answer: {answer}

    Reply only YES or NO.
    """

    return ask_llm(prompt).upper().startswith("YES")


# 6. Main Self-RAG function
def answer_customer_question(question, collection):
    # Retrieve documents
    documents = search_documents(question, collection)

    # Check retrieval relevance
    if not check_relevance(question, documents):
        return "No relevant documents found."

    # Generate answer
    answer = generate_answer(question, documents)

    # Self-evaluate answer
    if not check_support(answer, documents):
        return "Answer is not supported by the available documents."

    if not check_answer(question, answer):
        return "Unable to generate a satisfactory answer."

    return answer
