
import os
from typing import TypedDict

from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

from database import execute_db_query
from rag import search_policy

load_dotenv()

# Initialize LLM
llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
    temperature=0
)


# 1. Define State
class BankingState(TypedDict):
    question: str
    route: str
    result: str
    answer: str


# 2. Router Node
def router_node(state):

    question = state["question"]

    prompt = f"""
    Classify the question into one category.

    DB  - Account and transaction related questions.
    RAG - Banking policies and procedures.

    Question: {question}

    Return only DB or RAG.
    """

    response = llm.invoke(prompt)

    route = response.content.strip().upper()

    if route == "DB":
        return {"route": "db"}
    else:
        return {"route": "rag"}


# 3. Database Node
def db_node(state):

    result = execute_db_query(state["question"])

    return {"result": result}


# 4. RAG Node
def rag_node(state):

    result = search_policy(state["question"])

    return {"result": result}


# 5. Response Node
def response_node(state):

    prompt = f"""
    You are a Banking Assistant.

    User Question:
    {state['question']}

    Retrieved Information:
    {state['result']}

    Answer clearly using the retrieved information.
    Do not invent information.
    """

    response = llm.invoke(prompt)

    return {"answer": response.content}


# 6. Conditional Routing
def route_question(state):

    return state["route"]


# 7. Create LangGraph Workflow
workflow = StateGraph(BankingState)

workflow.add_node("router", router_node)
workflow.add_node("db", db_node)
workflow.add_node("rag", rag_node)
workflow.add_node("response", response_node)

workflow.add_edge(START, "router")

workflow.add_conditional_edges(
    "router",
    route_question,
    {
        "db": "db",
        "rag": "rag"
    }
)

workflow.add_edge("db", "response")
workflow.add_edge("rag", "response")

workflow.add_edge("response", END)

# Compile Graph
banking_graph = workflow.compile()