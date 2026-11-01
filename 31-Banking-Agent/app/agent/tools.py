"""
LangChain Tools = functions the LLM is allowed to call.
Each tool is a thin wrapper over the analytics / RAG layer.
The docstring is IMPORTANT - the LLM reads it to decide which tool to use.
"""
import json
from langchain_core.tools import tool

from app.services import analytics
from app.rag.vector_store import search_policies


def _to_json(data) -> str:
    return json.dumps(data, default=str)


@tool
def get_accounts_summary() -> str:
    """Get total accounts, total balance, and counts by status (ACTIVE/DORMANT/CLOSED) and type."""
    return _to_json(analytics.accounts_summary())


@tool
def get_account_details(account_id: str) -> str:
    """Get details of one account by account_id, e.g. AC1005."""
    return _to_json(analytics.account_details(account_id))


@tool
def get_incoming_outgoing(start_date: str = "", end_date: str = "", branch_id: str = "") -> str:
    """Get total incoming (credit) and outgoing (debit) amounts and net flow.
    Dates are YYYY-MM-DD (optional). branch_id like BR001 (optional)."""
    return _to_json(analytics.incoming_outgoing(start_date or None, end_date or None,
                                                branch_id or None))


@tool
def get_branch_revenue(start_date: str = "", end_date: str = "") -> str:
    """Get total revenue per branch (transaction fees + loan processing fees),
    sorted highest first. Dates are YYYY-MM-DD (optional)."""
    return _to_json(analytics.branch_revenue(start_date or None, end_date or None))


@tool
def get_loan_summary(start_date: str = "", end_date: str = "") -> str:
    """Get loan applications count, approved/pending/rejected counts, approval rate
    and approved amount by loan type. Dates are YYYY-MM-DD (optional)."""
    return _to_json(analytics.loan_summary(start_date or None, end_date or None))


@tool
def get_date_range_report(start_date: str, end_date: str) -> str:
    """Get a full report (cash flow, branch revenue, loans) for a date range. Dates are YYYY-MM-DD."""
    return _to_json(analytics.date_range_report(start_date, end_date))


@tool
def search_bank_policies(question: str) -> str:
    """Search the bank's policy documents (loan rules, account rules, fees, limits,
    employee handbook, leave, escalation). Use for any 'what is the rule/policy' question."""
    return search_policies(question)


DATA_TOOLS = [get_accounts_summary, get_account_details, get_incoming_outgoing,
              get_branch_revenue, get_loan_summary, get_date_range_report]
ALL_TOOLS = DATA_TOOLS + [search_bank_policies]
