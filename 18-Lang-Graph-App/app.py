import sqlite3
from typing import Literal, TypedDict

import httpx
from langchain_ollama import ChatOllama
from langgraph.graph import END, START, StateGraph

# ============================================================
# 1. GRAPH STATE
# ============================================================

class ChatState(TypedDict, total=False):
    question: str
    student_id: int
    category: str
    context: str
    answer: str

# ============================================================
# 2. SAMPLE DATABASE
# ============================================================

DB_NAME = "students.db"

def initialize_database() -> None:
    with sqlite3.connect(DB_NAME) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                course TEXT NOT NULL,
                fee_paid REAL NOT NULL,
                fee_due REAL NOT NULL,
                batch_time TEXT NOT NULL
            )
            """
        )

        connection.execute(
            """
            INSERT OR IGNORE INTO students
            (student_id, name, course, fee_paid, fee_due, batch_time)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                101,
                "Ravi Kumar",
                "GEN AI and Agentic AI with Python",
                9000,
                9000,
                "7:00 PM IST",
            ),
        )

        connection.commit()

# ============================================================
# 3. OLLAMA LLM
# ============================================================

llm = ChatOllama(
    model="llama3.2",
    temperature=0,
)

# ============================================================
# 4. CLASSIFIER NODE
# ============================================================

def classify_question(state: ChatState) -> dict:
    question = state["question"].lower()

    payment_words = [
        "fee", "payment", "paid", "pending amount", "due"
    ]

    course_words = [
        "course", "topics", "syllabus", "learn", "duration", "project"
    ]

    api_words = [
        "live", "api", "external", "service", "status"
    ]

    if any(word in question for word in payment_words):
        category = "payment"
    elif any(word in question for word in course_words):
        category = "course"
    elif any(word in question for word in api_words):
        category = "live"
    else:
        category = "general"

    print(f"Classifier selected: {category}")

    return {"category": category}

# ============================================================
# 5. ROUTING FUNCTION
# ============================================================

def route_question(
    state: ChatState,
) -> Literal["database", "rag", "api", "general"]:
    return state["category"]

# ============================================================
# 6. DATABASE NODE
# ============================================================

def database_node(state: ChatState) -> dict:
    print("Executing database node")

    student_id = state.get("student_id")

    if student_id is None:
        return {
            "context": (
                "Student ID was not provided. "
                "Payment information cannot be retrieved."
            )
        }

    with sqlite3.connect(DB_NAME) as connection:
        connection.row_factory = sqlite3.Row

        student = connection.execute(
            """
            SELECT student_id, name, course, fee_paid, fee_due, batch_time
            FROM students
            WHERE student_id = ?
            """,
            (student_id,),
        ).fetchone()

    if student is None:
        return {
            "context": f"No student exists with ID {student_id}."
        }

    context = f"""
Student ID: {student['student_id']}
Student name: {student['name']}
Course: {student['course']}
Fee paid: INR {student['fee_paid']}
Fee due: INR {student['fee_due']}
Batch time: {student['batch_time']}
""".strip()

    return {"context": context}

# ============================================================
# 7. RAG NODE
# ============================================================


COURSE_KNOWLEDGE = """
GEN AI and Agentic AI with Python is a four-month online training program.

The course covers Python, prompt engineering, LLM integration, LangChain,
LangGraph, RAG, vector databases, AI agents, Agentic AI workflows, FastAPI,
Streamlit, real-time projects and cloud deployment.

Students build projects such as document question-answering systems,
student-support chatbots, RAG applications, AI agents and automation assistants.

Students receive live classes, notes, backup videos, doubt clarification,
project guidance, certification and placement assistance.
"""

def rag_node(state: ChatState) -> dict:
    print("Executing RAG node")

    # This is simplified for teaching.
    # In production, retrieve relevant chunks from FAISS, Chroma, or Pinecone.
    return {"context": COURSE_KNOWLEDGE}


# ============================================================
# 8. API NODE
# ============================================================

def api_node(state: ChatState) -> dict:
    print("Executing API node")

    url = "https://jsonplaceholder.typicode.com/todos/1"

    try:
        response = httpx.get(url, timeout=5.0)
        response.raise_for_status()
        data = response.json()

        context = f"""
External service record ID: {data.get('id')}
Service message: {data.get('title')}
Completed: {data.get('completed')}
""".strip()

    except httpx.HTTPError as error:
        context = (
            "The external API is currently unavailable. "
            f"Error type: {type(error).__name__}"
        )

    return {"context": context}


# ============================================================
# 9. GENERAL NODE
# ============================================================

def general_node(state: ChatState) -> dict:
    print("Executing general node")

    return {
        "context": (
            "No private database, RAG, or external API "
            "information is required for this question."
        )
    }


# ============================================================
# 10. ANSWER NODE
# ============================================================

def generate_answer(state: ChatState) -> dict:
    print("Executing answer-generation node")

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

# ============================================================
# 11. BUILD THE GRAPH
# ============================================================

builder = StateGraph(ChatState)


builder.add_node("classify", classify_question)
builder.add_node("database", database_node)
builder.add_node("rag", rag_node)
builder.add_node("api", api_node)
builder.add_node("general", general_node)
builder.add_node("generate_answer", generate_answer)

builder.add_edge(START, "classify")


builder.add_conditional_edges(
    "classify",
    route_question,
    {
        "payment": "database",
        "course": "rag",
        "live": "api",
        "general": "general",
    },
)

builder.add_edge("database", "generate_answer")
builder.add_edge("rag", "generate_answer")
builder.add_edge("api", "generate_answer")
builder.add_edge("general", "generate_answer")


builder.add_edge("generate_answer", END)

graph = builder.compile()


# ============================================================
# 12. RUN THE GRAPH
# ============================================================

initialize_database()

print("\nSTUDENT SUPPORT CHATBOT")
print("Type 'exit' to stop.\n")


while True:
        question = input("You: ").strip()

        if question.lower() == "exit":
            print("Chatbot stopped.")
            break

        student_id_input = input(
            "Student ID, or press Enter: "
        ).strip()

        student_id = (
            int(student_id_input)
            if student_id_input
            else None
        )

        initial_state: ChatState = {
            "question": question,
        }

        if student_id is not None:
            initial_state["student_id"] = student_id

        final_state = graph.invoke(initial_state)

        print("\nBot:", final_state["answer"])
        print("Selected category:", final_state["category"])
        print("-" * 60)




