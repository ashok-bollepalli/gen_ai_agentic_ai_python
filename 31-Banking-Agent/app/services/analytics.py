"""
Data Analysis layer (MySQL + Pandas - no AI here).
  SQL   -> fetches only the rows we need (date range filter runs in MySQL)
  Pandas -> does the grouping / pivots / business calculations
Every function returns plain Python lists/dicts so FastAPI, MCP and
LangChain tools can all reuse the SAME business logic.
"""
import pandas as pd
from app.db import run_query


# ---------------- Read helpers ----------------
def _read_transactions(start=None, end=None, branch_id=None) -> pd.DataFrame:
    sql = "SELECT * FROM transactions WHERE 1=1"
    params = {}
    if start:
        sql += " AND txn_date >= :start"
        params["start"] = start
    if end:
        sql += " AND txn_date <= :end"
        params["end"] = end
    if branch_id:
        sql += " AND branch_id = :branch_id"
        params["branch_id"] = branch_id.upper()
    df = run_query(sql, params, date_cols=["txn_date"])
    return df.astype({"amount": float, "fee": float})


def _read_loans(start=None, end=None) -> pd.DataFrame:
    sql = "SELECT * FROM loans WHERE 1=1"
    params = {}
    if start:
        sql += " AND applied_date >= :start"
        params["start"] = start
    if end:
        sql += " AND applied_date <= :end"
        params["end"] = end
    df = run_query(sql, params, date_cols=["applied_date"])
    return df.astype({"amount": float, "processing_fee": float})


def _add_branch_name(df: pd.DataFrame) -> pd.DataFrame:
    branches = run_query("SELECT branch_id, branch_name FROM branches")
    return df.merge(branches, on="branch_id", how="left")


# ---------------- 1. Accounts summary ----------------
def accounts_summary() -> dict:
    acc = run_query("SELECT account_type, balance, status FROM accounts")
    return {
        "total_accounts": int(len(acc)),
        "total_balance": float(acc["balance"].astype(float).sum()),
        "by_status": acc["status"].value_counts().to_dict(),
        "by_type": acc["account_type"].value_counts().to_dict(),
    }


def account_details(account_id: str) -> dict:
    df = run_query("SELECT * FROM accounts WHERE account_id = :id", {"id": account_id.upper()})
    if df.empty:
        return {"error": f"Account {account_id} not found"}
    return df.astype(str).to_dict(orient="records")[0]


# ---------------- 2. Incoming vs Outgoing ----------------
def incoming_outgoing(start: str | None = None, end: str | None = None,
                      branch_id: str | None = None) -> dict:
    txn = _read_transactions(start, end, branch_id)
    incoming = float(txn.loc[txn.txn_type == "CREDIT", "amount"].sum())
    outgoing = float(txn.loc[txn.txn_type == "DEBIT", "amount"].sum())
    return {"incoming": incoming, "outgoing": outgoing,
            "net_flow": incoming - outgoing, "transaction_count": int(len(txn))}


def monthly_cash_flow(start: str | None = None, end: str | None = None) -> list[dict]:
    txn = _read_transactions(start, end)
    txn = txn.assign(month=txn["txn_date"].dt.strftime("%Y-%m"))
    pivot = txn.pivot_table(index="month", columns="txn_type", values="amount",
                            aggfunc="sum", fill_value=0).reset_index()
    pivot = pivot.rename(columns={"CREDIT": "incoming", "DEBIT": "outgoing"})
    return pivot.to_dict(orient="records")


# ---------------- 3. Branch revenue ----------------
def branch_revenue(start: str | None = None, end: str | None = None) -> list[dict]:
    """Revenue = transaction fees + loan processing fees."""
    txn = _read_transactions(start, end)
    loans = _read_loans(start, end)

    txn_fee = txn.groupby("branch_id")["fee"].sum().rename("transaction_fees")
    loan_fee = loans.groupby("branch_id")["processing_fee"].sum().rename("loan_fees")

    df = pd.concat([txn_fee, loan_fee], axis=1).fillna(0).reset_index()
    df["total_revenue"] = df["transaction_fees"] + df["loan_fees"]
    df = _add_branch_name(df).sort_values("total_revenue", ascending=False)
    return df.round(2).to_dict(orient="records")


# ---------------- 4. Loan approvals ----------------
def loan_summary(start: str | None = None, end: str | None = None) -> dict:
    loans = _read_loans(start, end)
    approved = loans[loans.status == "APPROVED"]
    return {
        "total_applications": int(len(loans)),
        "by_status": loans["status"].value_counts().to_dict(),
        "approval_rate_pct": round(len(approved) / max(len(loans), 1) * 100, 2),
        "approved_amount": float(approved["amount"].sum()),
        "approved_by_type": approved.groupby("loan_type")["amount"].sum().to_dict(),
    }


def loans_by_branch(start: str | None = None, end: str | None = None) -> list[dict]:
    loans = _read_loans(start, end)
    df = loans.pivot_table(index="branch_id", columns="status", values="loan_id",
                           aggfunc="count", fill_value=0).reset_index()
    return _add_branch_name(df).to_dict(orient="records")


# ---------------- 5. Date range report (everything together) ----------------
def date_range_report(start: str, end: str) -> dict:
    return {
        "period": {"start": start, "end": end},
        "cash_flow": incoming_outgoing(start, end),
        "branch_revenue": branch_revenue(start, end),
        "loans": loan_summary(start, end),
    }
