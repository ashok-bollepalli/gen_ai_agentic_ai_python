"""
Database connection (MySQL through SQLAlchemy + PyMySQL).
One engine for the whole app; it keeps a small pool of connections open.
"""
from functools import lru_cache
import pandas as pd
from sqlalchemy import create_engine, text

from app.config import DATABASE_URL


@lru_cache
def get_engine():
    # pool_pre_ping = reconnect automatically if MySQL closed an idle connection
    return create_engine(DATABASE_URL, pool_pre_ping=True)


def run_query(sql: str, params: dict | None = None, date_cols: list[str] | None = None) -> pd.DataFrame:
    """Run a SELECT and get the result as a Pandas DataFrame.
    Always pass values through `params` (never f-strings) to avoid SQL injection."""
    with get_engine().connect() as conn:
        return pd.read_sql(text(sql), conn, params=params or {}, parse_dates=date_cols)
