"""
Service layer = business logic.
- Validates / defaults the date range
- Calls the repository
- Adds simple calculated values (totals, approval rate, net flow)

Used by BOTH the FastAPI dashboard endpoints AND the MCP server tools.
(Same logic, two doors -> that is clean architecture.)
"""
from datetime import date, timedelta

from app.repositories import bank_repository as repo


def _date_range(start_date: str | None, end_date: str | None) -> tuple[str, str]:
    """Default = last 90 days. Dates are 'YYYY-MM-DD' strings."""
    end = date.fromisoformat(end_date) if end_date else date.today()
    start = date.fromisoformat(start_date) if start_date else end - timedelta(days=90)
    if start > end:
        raise ValueError("start_date must be before end_date")
    return start.isoformat(), end.isoformat()


def list_branches() -> list[dict]:
    return repo.get_branches()


def accounts_summary() -> dict:
    rows = repo.get_accounts_summary()
    return {
        "total_accounts": sum(r["total_accounts"] for r in rows),
        "total_balance": round(sum(r["total_balance"] for r in rows), 2),
        "by_branch": rows,
    }


def branch_revenue(start_date: str | None = None, end_date: str | None = None) -> dict:
    start, end = _date_range(start_date, end_date)
    rows = repo.get_branch_revenue(start, end)
    return {
        "start_date": start,
        "end_date": end,
        "total_revenue": round(sum(r["total_revenue"] for r in rows), 2),
        "by_branch": rows,
    }


def cash_flow(start_date: str | None = None, end_date: str | None = None) -> dict:
    start, end = _date_range(start_date, end_date)
    rows = repo.get_cash_flow(start, end)
    for r in rows:
        r["net_flow"] = round(r["incoming"] - r["outgoing"], 2)
    return {
        "start_date": start,
        "end_date": end,
        "total_incoming": round(sum(r["incoming"] for r in rows), 2),
        "total_outgoing": round(sum(r["outgoing"] for r in rows), 2),
        "by_branch": rows,
    }


def monthly_trend(start_date: str | None = None, end_date: str | None = None) -> dict:
    start, end = _date_range(start_date, end_date)
    return {"start_date": start, "end_date": end, "months": repo.get_monthly_trend(start, end)}


def loan_approvals(start_date: str | None = None, end_date: str | None = None) -> dict:
    start, end = _date_range(start_date, end_date)
    by_type = repo.get_loans_by_type(start, end)
    for r in by_type:
        r["approval_rate_pct"] = round(100 * r["approved"] / r["applications"], 1) if r["applications"] else 0
    total_apps = sum(r["applications"] for r in by_type)
    total_approved = sum(r["approved"] for r in by_type)
    return {
        "start_date": start,
        "end_date": end,
        "total_applications": total_apps,
        "total_approved": total_approved,
        "approval_rate_pct": round(100 * total_approved / total_apps, 1) if total_apps else 0,
        "by_type": by_type,
        "by_branch_status": repo.get_loan_summary(start, end),
    }


def top_accounts(limit: int = 10) -> list[dict]:
    return repo.get_top_accounts(max(1, min(limit, 50)))


def full_report(start_date: str | None = None, end_date: str | None = None) -> dict:
    """One combined report for a date range."""
    return {
        "revenue": branch_revenue(start_date, end_date),
        "cash_flow": cash_flow(start_date, end_date),
        "loans": loan_approvals(start_date, end_date),
    }
