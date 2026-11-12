"""
Database connection (SQLAlchemy engine for AWS RDS MySQL).
One engine for the whole app -> connection pooling for free.
"""
from datetime import date, datetime
from decimal import Decimal
from functools import lru_cache

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from app.core.config import get_settings


@lru_cache
def get_engine() -> Engine:
    settings = get_settings()
    return create_engine(settings.database_url, pool_pre_ping=True, pool_recycle=3600)


def _clean(value):
    """Make DB values JSON friendly (Decimal -> float, date -> str)."""
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return value


def fetch_all(sql: str, params: dict | None = None) -> list[dict]:
    """Run a SELECT query and return a list of plain dicts."""
    with get_engine().connect() as conn:
        rows = conn.execute(text(sql), params or {}).mappings().all()
    return [{k: _clean(v) for k, v in row.items()} for row in rows]
