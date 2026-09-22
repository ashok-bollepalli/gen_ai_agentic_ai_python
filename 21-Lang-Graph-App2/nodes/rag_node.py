from state.chat_state import ChatState
from knowledge.course_knowledge import COURSE_KNOWLEDGE

def rag_node(state:ChatState) -> dict:
    print("Executing rag node")

    # Simplified RAG for teaching.
    # In production, retrieve relevant chunks from
    # Chroma, FAISS, Pinecone, etc.

    return {"context": COURSE_KNOWLEDGE}

