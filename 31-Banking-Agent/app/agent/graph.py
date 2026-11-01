"""
LangGraph Agent - the "brain" of the Employee AI Assistant.

Flow:
            ┌──────────┐
  START ──▶ │  router  │  (LLM decides: analytics / policy / general)
            └────┬─────┘
       ┌─────────┼──────────────┐
       ▼         ▼              ▼
   analyst    policy_rag     general
     │  ▲         │              │
     ▼  │         ▼              ▼
    tools        END            END
 (loop until analyst has the answer, then END)
"""
from datetime import date
from functools import lru_cache
from typing import Literal

from pydantic import BaseModel
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

from app.config import LLM_MODEL
from app.agent.tools import DATA_TOOLS
from app.rag.vector_store import search_policies


# ---------- 1. State: chat messages + the route the router picked ----------
class AgentState(MessagesState):
    route: str


# ---------- 2. Router output schema (structured output) ----------
class Route(BaseModel):
    route: Literal["analytics", "policy", "general"]


ANALYST_PROMPT = f"""You are a banking data analyst assistant for bank employees.
Today is {date.today()}. Use the tools to fetch real numbers - never guess numbers.
Convert phrases like 'last month' or 'March 2026' into YYYY-MM-DD dates.
Show amounts in Indian Rupees (Rs) with commas. Keep answers short, use a small table if helpful."""

POLICY_PROMPT = """You are a helpful bank policy assistant for employees.
Answer ONLY from the context below. If the answer is not in the context, say
"I could not find this in the bank policies." Mention the source file at the end.

Context:
{context}"""


def build_graph(tools=DATA_TOOLS):
    """Build the agent. `tools` can be local LangChain tools or tools loaded from MCP."""
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0)
    llm_with_tools = llm.bind_tools(tools)

    # ---------- 3. Nodes (plain Python functions: state in -> update out) ----------
    def router(state: AgentState):
        question = state["messages"][-1].content
        decision = llm.with_structured_output(Route).invoke(
            "Classify this bank employee question.\n"
            "analytics = numbers about accounts, transactions, revenue, loans, reports\n"
            "policy = rules, fees, limits, eligibility, HR / leave / escalation\n"
            f"general = greetings or anything else\n\nQuestion: {question}")
        return {"route": decision.route}

    def analyst(state: AgentState):
        response = llm_with_tools.invoke([SystemMessage(ANALYST_PROMPT)] + state["messages"])
        return {"messages": [response]}

    def policy_rag(state: AgentState):
        question = state["messages"][-1].content
        context = search_policies(question)                     # Retrieve
        prompt = SystemMessage(POLICY_PROMPT.format(context=context))  # Augment
        response = llm.invoke([prompt] + state["messages"])     # Generate
        return {"messages": [response]}

    def general(state: AgentState):
        response = llm.invoke([SystemMessage(
            "You are a friendly bank employee assistant. You can help with account, "
            "transaction, revenue and loan analytics, and bank policy questions. "
            "Politely decline unrelated requests.")] + state["messages"])
        return {"messages": [response]}

    # ---------- 4. Wire the graph ----------
    graph = StateGraph(AgentState)
    graph.add_node("router", router)
    graph.add_node("analyst", analyst)
    graph.add_node("tools", ToolNode(tools))
    graph.add_node("policy_rag", policy_rag)
    graph.add_node("general", general)

    graph.add_edge(START, "router")
    graph.add_conditional_edges("router", lambda s: s["route"],
                                {"analytics": "analyst", "policy": "policy_rag",
                                 "general": "general"})
    graph.add_conditional_edges("analyst", tools_condition)  # tool call? -> tools, else END
    graph.add_edge("tools", "analyst")
    graph.add_edge("policy_rag", END)
    graph.add_edge("general", END)

    # MemorySaver = remembers chat history per thread_id (session)
    return graph.compile(checkpointer=MemorySaver())


@lru_cache
def get_agent():
    return build_graph()


def ask(question: str, session_id: str = "default") -> dict:
    """Simple helper used by FastAPI."""
    result = get_agent().invoke({"messages": [("user", question)]},
                                config={"configurable": {"thread_id": session_id}})
    return {"answer": result["messages"][-1].content, "route": result.get("route")}


if __name__ == "__main__":
    print(ask("Which branch earned the highest revenue in March 2026?")["answer"])
