"""
MCP Client demo - the SAME LangGraph agent, but tools come from the MCP server
instead of local Python functions. This shows that tools are "pluggable".

Run:  python -m mcp_server.client_demo
"""
import asyncio
import sys

from langchain_mcp_adapters.client import MultiServerMCPClient
from app.agent.graph import build_graph


async def main():
    # 1. Connect to our MCP server (it is started automatically as a subprocess)
    client = MultiServerMCPClient({
        "bank": {"command": sys.executable, "args": ["-m", "mcp_server.server"],
                 "transport": "stdio"}
    })

    # 2. Discover tools from the server
    tools = await client.get_tools()
    print("🔌 Tools loaded from MCP:", [t.name for t in tools])

    # 3. Give those tools to the LangGraph agent
    agent = build_graph(tools)
    config = {"configurable": {"thread_id": "mcp-demo"}}

    for q in ["What is the loan approval rate in 2026?",
              "Compare incoming vs outgoing money for branch BR001 in April 2026"]:
        result = await agent.ainvoke({"messages": [("user", q)]}, config=config)
        print(f"\n❓ {q}\n🤖 {result['messages'][-1].content}")


if __name__ == "__main__":
    asyncio.run(main())
