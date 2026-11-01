"""
Create the tables in MySQL and load the sample data.

Run:  python -m data.seed_mysql
Steps: 1) run schema.sql  2) generate data  3) insert with pandas.to_sql
"""
from sqlalchemy import text

from app.config import SCHEMA_FILE
from app.db import get_engine
from data.generate_data import build_data

# Parents first, so foreign keys are satisfied
LOAD_ORDER = ["branches", "accounts", "transactions", "loans"]


def create_tables(engine):
    statements = [s.strip() for s in SCHEMA_FILE.read_text().split(";")]
    with engine.begin() as conn:
        for sql in statements:
            sql = "\n".join(l for l in sql.splitlines() if not l.strip().startswith("--"))
            if sql.strip():
                conn.execute(text(sql))
    print("✅ Tables created")


def load_data(engine):
    data = build_data()
    for table in LOAD_ORDER:
        data[table].to_sql(table, engine, if_exists="append", index=False, chunksize=500)
        print(f"✅ {table}: {len(data[table])} rows inserted")


if __name__ == "__main__":
    engine = get_engine()
    create_tables(engine)
    load_data(engine)
