"""
MCP Server = exposes bank analytics as TOOLS over the Model Context Protocol.

Any MCP client (our LangGraph agent, Claude Desktop, Cursor ...) can discover
and call these tools. The tools just call the service layer.

Run:  python -m app.mcp_server.server     (listens on http://0.0.0.0:8001/mcp)
"""
from mcp.server.fastmcp import FastMCP

from app.services import analytics_service as svc

mcp = FastMCP("bank-analytics", host="0.0.0.0", port=8001)


@mcp.tool()
def list_branches() -> list[dict]:
    """List all bank branches with id, name, city and state."""
    return svc.list_branches()


@mcp.tool()
def get_accounts_summary() -> dict:
    """Account counts, active accounts and total balance by branch and account type."""
    return svc.accounts_summary()


@mcp.tool()
def get_branch_revenue(start_date: str = "", end_date: str = "") -> dict:
    """Bank revenue (fees + interest earned) per branch for a date range.
    Dates format: YYYY-MM-DD. Empty = last 90 days."""
    return svc.branch_revenue(start_date or None, end_date or None)


@mcp.tool()
def get_cash_flow(start_date: str = "", end_date: str = "") -> dict:
    """Incoming (credit) and outgoing (debit) amounts and net flow per branch for a date range.
    Dates format: YYYY-MM-DD. Empty = last 90 days."""
    return svc.cash_flow(start_date or None, end_date or None)


@mcp.tool()
def get_monthly_trend(start_date: str = "", end_date: str = "") -> dict:
    """Month-by-month incoming, outgoing and revenue totals for a date range.
    Dates format: YYYY-MM-DD. Empty = last 90 days."""
    return svc.monthly_trend(start_date or None, end_date or None)


@mcp.tool()
def get_loan_approvals(start_date: str = "", end_date: str = "") -> dict:
    """Loan applications, approvals, approval rate and approved amount by loan type and branch
    for a date range (based on applied date). Dates format: YYYY-MM-DD. Empty = last 90 days."""
    return svc.loan_approvals(start_date or None, end_date or None)


@mcp.tool()
def get_top_accounts(limit: int = 10) -> list[dict]:
    """Top active accounts by balance (max 50)."""
    return svc.top_accounts(limit)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
