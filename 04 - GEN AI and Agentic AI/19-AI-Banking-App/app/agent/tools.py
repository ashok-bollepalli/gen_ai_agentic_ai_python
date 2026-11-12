"""
Agent tools come from TWO places:
  1. MCP server  -> bank analytics tools (remote, discovered at runtime)
  2. Local tool  -> RAG search over bank policy documents
"""
from langchain_core.tools import tool
from langchain_mcp_adapters.client import MultiServerMCPClient

from app.core.config import get_settings
from app.rag.vector_store import search_policies


@tool
def search_bank_policies(question: str) -> str:
    """Search bank policy documents (loans, KYC, accounts, fees, employee FAQ).
    Use this for any 'what is the rule / process / policy' question."""
    return search_policies(question)


async def load_mcp_tools() -> list:
    """Connect to the MCP server and get its tools as LangChain tools."""
    client = MultiServerMCPClient({
        "bank": {"url": get_settings().mcp_server_url, "transport": "streamable_http"}
    })
    return await client.get_tools()


async def get_all_tools() -> list:
    return [*await load_mcp_tools(), search_bank_policies]
