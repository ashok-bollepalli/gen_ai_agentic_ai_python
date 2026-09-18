from langgraph.graph import END, START, StateGraph

from state.chat_state import ChatState
from nodes.classifier import classify_question
from nodes.database_node import database_node
from nodes.rag_node import rag_node
from nodes.api_node import api_node
from nodes.general_node import general_node
from nodes.answer_node import generate_answer
from graph.router import route_question

def build_graph():
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
            "database" : "database",
            "rag" : "rag",
            "api" : "api",
            "general" : "general",
        },
    )

    builder.add_edge("database", "generate_answer")
    builder.add_edge("rag", "generate_answer")
    builder.add_edge("api", "generate_answer")
    builder.add_edge("general", "generate_answer")


    builder.add_edge("generate_answer", END)

    return builder.compile()


graph = build_graph()
