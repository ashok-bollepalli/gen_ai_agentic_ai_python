"""
LangGraph agent (ReAct loop drawn as a graph):

    START --> agent --(tool calls?)--> tools --> agent --> ... --> END

- agent node : LLM decides -> answer directly OR call tool(s)
- tools node : runs the tools (MCP analytics / RAG search)
- MemorySaver: remembers the chat per thread_id (conversation memory)
"""
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from app.agent.prompts import get_system_prompt
from app.agent.tools import get_all_tools
from app.core.config import get_settings


def build_graph(tools: list):
    settings = get_settings()
    llm = ChatOpenAI(model=settings.openai_model, api_key=settings.openai_api_key,
                     temperature=0).bind_tools(tools)

    async def agent_node(state: MessagesState):
        messages = [SystemMessage(get_system_prompt())] + state["messages"]
        response = await llm.ainvoke(messages)
        return {"messages": [response]}

    graph = StateGraph(MessagesState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", ToolNode(tools))

    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", tools_condition, {"tools": "tools", END: END})
    graph.add_edge("tools", "agent")

    return graph.compile(checkpointer=MemorySaver())


class BankAgent:
    """Small wrapper so FastAPI only calls: await agent.chat(question, session_id)."""

    def __init__(self):
        self.graph = None

    async def _ensure_ready(self):
        if self.graph is None:  # build lazily -> MCP server can start after API
            self.graph = build_graph(await get_all_tools())

    async def chat(self, question: str, session_id: str) -> dict:
        await self._ensure_ready()
        result = await self.graph.ainvoke(
            {"messages": [HumanMessage(question)]},
            config={"configurable": {"thread_id": session_id}, "recursion_limit": 15},
        )
        # Which tools were used in THIS turn (nice to show students)
        tools_used = []
        for msg in reversed(result["messages"]):
            if isinstance(msg, HumanMessage):
                break
            for call in getattr(msg, "tool_calls", []) or []:
                tools_used.append(call["name"])
        return {"answer": result["messages"][-1].content, "tools_used": list(reversed(tools_used))}
