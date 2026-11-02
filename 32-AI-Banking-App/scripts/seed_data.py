"""
Create tables and load sample banking data into MySQL (AWS RDS).

Run:  python -m scripts.seed_data
"""
import random
from datetime import date, timedelta
from pathlib import Path

from sqlalchemy import text

from app.db.connection import get_engine

random.seed(42)

BRANCHES = [
    ("Hyderabad Main", "Hyderabad", "Telangana"),
    ("Bengaluru MG Road", "Bengaluru", "Karnataka"),
    ("Chennai T Nagar", "Chennai", "Tamil Nadu"),
    ("Mumbai Fort", "Mumbai", "Maharashtra"),
    ("Pune Shivajinagar", "Pune", "Maharashtra"),
]
FIRST = ["Ravi", "Sita", "Kiran", "Anil", "Priya", "Rahul", "Divya", "Arjun", "Meena", "Suresh",
         "Lakshmi", "Vijay", "Kavya", "Naveen", "Swathi", "Manoj", "Deepa", "Harish", "Pooja", "Ajay"]
LAST = ["Reddy", "Sharma", "Kumar", "Rao", "Iyer", "Patel", "Naidu", "Gupta", "Verma", "Menon"]

START_DATE = date(2025, 1, 1)
END_DATE = date(2026, 10, 31)


def random_date(start: date = START_DATE, end: date = END_DATE) -> date:
    return start + timedelta(days=random.randint(0, (end - start).days))


def create_tables(conn):
    sql = Path(__file__).resolve().parents[1].joinpath("app/db/schema.sql").read_text()
    for statement in sql.split(";"):
        lines = [l for l in statement.splitlines() if not l.strip().startswith("--")]
        if "".join(lines).strip():
            conn.execute(text("\n".join(lines)))


def clear_tables(conn):
    for table in ["transactions", "loans", "accounts", "branches"]:
        conn.execute(text(f"DELETE FROM {table}"))
        conn.execute(text(f"ALTER TABLE {table} AUTO_INCREMENT = 1"))


def seed():
    engine = get_engine()
    with engine.begin() as conn:  # begin() = auto commit at the end
        create_tables(conn)
        clear_tables(conn)

        # 1. Branches
        conn.execute(
            text("INSERT INTO branches (branch_name, city, state, opened_on) "
                 "VALUES (:name, :city, :state, :opened_on)"),
            [{"name": n, "city": c, "state": s, "opened_on": date(2015 + i, 4, 1)}
             for i, (n, c, s) in enumerate(BRANCHES)],
        )

        # 2. Accounts (200)
        accounts = []
        for _ in range(200):
            accounts.append({
                "customer_name": f"{random.choice(FIRST)} {random.choice(LAST)}",
                "branch_id": random.randint(1, len(BRANCHES)),
                "account_type": random.choice(["SAVINGS", "SAVINGS", "CURRENT"]),
                "balance": round(random.uniform(5_000, 2_500_000), 2),
                "status": random.choices(["ACTIVE", "DORMANT", "CLOSED"], [85, 10, 5])[0],
                "opened_on": random_date(date(2018, 1, 1), END_DATE),
            })
        conn.execute(
            text("INSERT INTO accounts (customer_name, branch_id, account_type, balance, status, opened_on) "
                 "VALUES (:customer_name, :branch_id, :account_type, :balance, :status, :opened_on)"),
            accounts,
        )

        # 3. Loans (150)
        loan_ranges = {"HOME": (1_500_000, 8_000_000, 8.5), "PERSONAL": (50_000, 1_000_000, 12.5),
                       "CAR": (300_000, 1_500_000, 9.5), "EDUCATION": (200_000, 2_000_000, 10.0)}
        loans = []
        for _ in range(150):
            acc_id = random.randint(1, 200)
            loan_type = random.choice(list(loan_ranges))
            low, high, rate = loan_ranges[loan_type]
            loans.append({
                "account_id": acc_id,
                "branch_id": accounts[acc_id - 1]["branch_id"],
                "loan_type": loan_type,
                "amount": round(random.uniform(low, high), -3),
                "interest_rate": rate,
                "status": random.choices(["APPROVED", "REJECTED", "PENDING"], [60, 25, 15])[0],
                "applied_on": random_date(),
            })
        conn.execute(
            text("INSERT INTO loans (account_id, branch_id, loan_type, amount, interest_rate, status, applied_on) "
                 "VALUES (:account_id, :branch_id, :loan_type, :amount, :interest_rate, :status, :applied_on)"),
            loans,
        )

        # 4. Transactions (6000)
        txns = []
        for _ in range(6000):
            acc_id = random.randint(1, 200)
            category = random.choices(
                ["DEPOSIT", "WITHDRAWAL", "TRANSFER_IN", "TRANSFER_OUT", "FEE", "INTEREST"],
                [30, 25, 15, 15, 10, 5])[0]
            txn_type = "CREDIT" if category in ("DEPOSIT", "TRANSFER_IN") else "DEBIT"
            if category in ("FEE", "INTEREST"):
                amount = round(random.uniform(100, 15_000), 2)   # bank revenue
            else:
                amount = round(random.uniform(1_000, 200_000), 2)
            txns.append({
                "account_id": acc_id,
                "branch_id": accounts[acc_id - 1]["branch_id"],
                "txn_type": txn_type,
                "category": category.replace("_IN", "").replace("_OUT", ""),
                "amount": amount,
                "txn_date": random_date(),
            })
        conn.execute(
            text("INSERT INTO transactions (account_id, branch_id, txn_type, category, amount, txn_date) "
                 "VALUES (:account_id, :branch_id, :txn_type, :category, :amount, :txn_date)"),
            txns,
        )

    print("Seeded: 5 branches, 200 accounts, 150 loans, 6000 transactions")


if __name__ == "__main__":
    seed()
