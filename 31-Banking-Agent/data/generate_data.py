"""
Sample banking data generator (pure Pandas, no database code here).
build_data() returns 4 DataFrames; data/seed_mysql.py inserts them into MySQL.
"""
import numpy as np
import pandas as pd


def build_data() -> dict[str, pd.DataFrame]:
    np.random.seed(42)  # same data for every student

    # ---------- Branches ----------
    branches = pd.DataFrame({
        "branch_id": ["BR001", "BR002", "BR003", "BR004", "BR005"],
        "branch_name": ["Hyderabad Main", "Bangalore MG Road", "Chennai T Nagar",
                        "Mumbai Andheri", "Delhi CP"],
        "city": ["Hyderabad", "Bangalore", "Chennai", "Mumbai", "Delhi"],
    })

    # ---------- Accounts ----------
    n_accounts = 200
    accounts = pd.DataFrame({
        "account_id": [f"AC{1000 + i}" for i in range(n_accounts)],
        "customer_name": [f"Customer {i + 1}" for i in range(n_accounts)],
        "branch_id": np.random.choice(branches.branch_id, n_accounts),
        "account_type": np.random.choice(["SAVINGS", "CURRENT"], n_accounts, p=[0.7, 0.3]),
        "balance": np.random.randint(5_000, 5_00_000, n_accounts),
        "opened_date": pd.to_datetime("2022-01-01")
                       + pd.to_timedelta(np.random.randint(0, 1000, n_accounts), unit="D"),
        "status": np.random.choice(["ACTIVE", "DORMANT", "CLOSED"], n_accounts, p=[0.85, 0.1, 0.05]),
    })

    # ---------- Transactions (CREDIT = incoming, DEBIT = outgoing) ----------
    n_txn = 3000
    txn_accounts = np.random.choice(accounts.account_id, n_txn)
    branch_map = dict(zip(accounts.account_id, accounts.branch_id))
    transactions = pd.DataFrame({
        "txn_id": [f"TX{100000 + i}" for i in range(n_txn)],
        "account_id": txn_accounts,
        "branch_id": [branch_map[a] for a in txn_accounts],
        "txn_date": pd.to_datetime("2026-01-01")
                    + pd.to_timedelta(np.random.randint(0, 300, n_txn), unit="D"),
        "txn_type": np.random.choice(["CREDIT", "DEBIT"], n_txn),
        "channel": np.random.choice(["UPI", "NEFT", "ATM", "BRANCH"], n_txn),
        "amount": np.random.randint(500, 1_00_000, n_txn),
    })
    # Bank revenue = fee charged on each transaction (simple rule: 0.5%)
    transactions["fee"] = (transactions["amount"] * 0.005).round(2)

    # ---------- Loans ----------
    n_loans = 300
    loans = pd.DataFrame({
        "loan_id": [f"LN{5000 + i}" for i in range(n_loans)],
        "account_id": np.random.choice(accounts.account_id, n_loans),
        "loan_type": np.random.choice(["HOME", "PERSONAL", "CAR", "EDUCATION"], n_loans),
        "amount": np.random.randint(50_000, 50_00_000, n_loans),
        "credit_score": np.random.randint(550, 850, n_loans),
        "applied_date": pd.to_datetime("2026-01-01")
                        + pd.to_timedelta(np.random.randint(0, 300, n_loans), unit="D"),
    })
    loans["branch_id"] = loans["account_id"].map(branch_map)
    # Simple rule: score >= 700 approved, 650-699 pending, else rejected
    loans["status"] = np.select(
        [loans.credit_score >= 700, loans.credit_score >= 650],
        ["APPROVED", "PENDING"], default="REJECTED")
    # Bank revenue from loans = 1% processing fee on approved loans
    loans["processing_fee"] = np.where(loans.status == "APPROVED", loans.amount * 0.01, 0)

    return {"branches": branches, "accounts": accounts,
            "transactions": transactions, "loans": loans}
