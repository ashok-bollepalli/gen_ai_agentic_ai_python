"""
MCP Server - exposes our banking tools using the Model Context Protocol.
Any MCP client (Claude Desktop, Cursor, VS Code, or our LangGraph agent)
can discover and call these tools.

Run:  python -m mcp_server.server        (stdio transport)
"""
from mcp.server.fastmcp import FastMCP

from app.services import analytics
from app.rag.vector_store import search_policies

mcp = FastMCP("bank-analytics")


@mcp.tool()
def get_accounts_summary() -> dict:
    """Get total accounts, total balance, and counts by status and type."""
    return analytics.accounts_summary()


@mcp.tool()
def get_account_details(account_id: str) -> dict:
    """Get details of one account by account_id, e.g. AC1005."""
    return analytics.account_details(account_id)


@mcp.tool()
def get_incoming_outgoing(start_date: str = "", end_date: str = "", branch_id: str = "") -> dict:
    """Total incoming (credit) and outgoing (debit) amounts. Dates YYYY-MM-DD, branch like BR001 (all optional)."""
    return analytics.incoming_outgoing(start_date or None, end_date or None, branch_id or None)


@mcp.tool()
def get_branch_revenue(start_date: str = "", end_date: str = "") -> list:
    """Revenue per branch (transaction fees + loan processing fees). Dates YYYY-MM-DD (optional)."""
    return analytics.branch_revenue(start_date or None, end_date or None)


@mcp.tool()
def get_loan_summary(start_date: str = "", end_date: str = "") -> dict:
    """Loan applications, approval rate and approved amounts. Dates YYYY-MM-DD (optional)."""
    return analytics.loan_summary(start_date or None, end_date or None)


@mcp.tool()
def get_date_range_report(start_date: str, end_date: str) -> dict:
    """Full report (cash flow, branch revenue, loans) for a date range. Dates YYYY-MM-DD."""
    return analytics.date_range_report(start_date, end_date)


@mcp.tool()
def search_bank_policies(question: str) -> str:
    """Search bank policy documents (loans, accounts, fees, limits, employee handbook)."""
    return search_policies(question)


if __name__ == "__main__":
    mcp.run(transport="stdio")
