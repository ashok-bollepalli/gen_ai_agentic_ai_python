from state.chat_state import ChatState
from llm.ollama_client import get_llm

llm = get_llm()

def generate_answer(state: ChatState) -> dict:
    print("Executing Answer-Generation node")

    prompt = f"""
    You are a student-support assistant.

    Answer the question using the supplied context.

    Rules:
    1. Do not invent student, fee, course, or API information.
    2. Give a clear and concise answer.
    3. If information is unavailable, say so.
    4. Do not mention internal graph nodes.

    Question:
    {state['question']}

    Question category:
    {state['category']}

    Context:
    {state['context']}
    """

    response = llm.invoke(prompt)

    return {"answer": response.content}
