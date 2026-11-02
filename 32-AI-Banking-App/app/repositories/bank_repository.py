"""
Repository layer = ONLY SQL.
No business rules here. Every function takes a date range and returns list[dict].
"""
from app.db.connection import fetch_all

# Bank revenue = money the bank earns (fees + interest collected)
REVENUE_CATEGORIES = "('FEE', 'INTEREST')"


def get_branches() -> list[dict]:
    return fetch_all("SELECT branch_id, branch_name, city, state FROM branches ORDER BY branch_id")


def get_accounts_summary() -> list[dict]:
    sql = """
        SELECT b.branch_name,
               a.account_type,
               COUNT(*)                                        AS total_accounts,
               COUNT(CASE WHEN a.status = 'ACTIVE' THEN 1 END)  AS active_accounts,
               ROUND(SUM(a.balance), 2)                        AS total_balance
        FROM accounts a
        JOIN branches b ON b.branch_id = a.branch_id
        GROUP BY b.branch_name, a.account_type
        ORDER BY b.branch_name, a.account_type
    """
    return fetch_all(sql)


def get_branch_revenue(start_date: str, end_date: str) -> list[dict]:
    sql = f"""
        SELECT b.branch_name,
               ROUND(SUM(t.amount), 2) AS total_revenue
        FROM transactions t
        JOIN branches b ON b.branch_id = t.branch_id
        WHERE t.category IN {REVENUE_CATEGORIES}
          AND t.txn_date BETWEEN :start AND :end
        GROUP BY b.branch_name
        ORDER BY total_revenue DESC
    """
    return fetch_all(sql, {"start": start_date, "end": end_date})


def get_cash_flow(start_date: str, end_date: str) -> list[dict]:
    """Incoming (CREDIT) vs outgoing (DEBIT) amount per branch."""
    sql = """
        SELECT b.branch_name,
               ROUND(SUM(CASE WHEN t.txn_type = 'CREDIT' THEN t.amount ELSE 0 END), 2) AS incoming,
               ROUND(SUM(CASE WHEN t.txn_type = 'DEBIT'  THEN t.amount ELSE 0 END), 2) AS outgoing
        FROM transactions t
        JOIN branches b ON b.branch_id = t.branch_id
        WHERE t.txn_date BETWEEN :start AND :end
        GROUP BY b.branch_name
        ORDER BY b.branch_name
    """
    return fetch_all(sql, {"start": start_date, "end": end_date})


def get_monthly_trend(start_date: str, end_date: str) -> list[dict]:
    sql = f"""
        SELECT DATE_FORMAT(t.txn_date, '%Y-%m') AS month,
               ROUND(SUM(CASE WHEN t.txn_type = 'CREDIT' THEN t.amount ELSE 0 END), 2) AS incoming,
               ROUND(SUM(CASE WHEN t.txn_type = 'DEBIT'  THEN t.amount ELSE 0 END), 2) AS outgoing,
               ROUND(SUM(CASE WHEN t.category IN {REVENUE_CATEGORIES} THEN t.amount ELSE 0 END), 2) AS revenue
        FROM transactions t
        WHERE t.txn_date BETWEEN :start AND :end
        GROUP BY month
        ORDER BY month
    """
    return fetch_all(sql, {"start": start_date, "end": end_date})


def get_loan_summary(start_date: str, end_date: str) -> list[dict]:
    sql = """
        SELECT b.branch_name,
               l.status,
               COUNT(*)                AS loan_count,
               ROUND(SUM(l.amount), 2) AS total_amount
        FROM loans l
        JOIN branches b ON b.branch_id = l.branch_id
        WHERE l.applied_on BETWEEN :start AND :end
        GROUP BY b.branch_name, l.status
        ORDER BY b.branch_name, l.status
    """
    return fetch_all(sql, {"start": start_date, "end": end_date})


def get_loans_by_type(start_date: str, end_date: str) -> list[dict]:
    sql = """
        SELECT loan_type,
               COUNT(*)                                             AS applications,
               COUNT(CASE WHEN status = 'APPROVED' THEN 1 END)  AS approved,
               ROUND(SUM(CASE WHEN status = 'APPROVED' THEN amount ELSE 0 END), 2) AS approved_amount
        FROM loans
        WHERE applied_on BETWEEN :start AND :end
        GROUP BY loan_type
        ORDER BY approved_amount DESC
    """
    return fetch_all(sql, {"start": start_date, "end": end_date})


def get_top_accounts(limit: int) -> list[dict]:
    sql = """
        SELECT a.account_id, a.customer_name, b.branch_name, a.account_type, a.balance
        FROM accounts a
        JOIN branches b ON b.branch_id = a.branch_id
        WHERE a.status = 'ACTIVE'
        ORDER BY a.balance DESC
        LIMIT :limit
    """
    return fetch_all(sql, {"limit": limit})
