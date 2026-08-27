"""Database engine and session helpers.

SQLite via SQLAlchemy. ``init_db`` creates tables from the ORM metadata; there
is no migration framework in the MVP because the schema is small and the DB is
local and disposable. If the schema outgrows this, add Alembic later.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_settings
from app.database.models import Base


def _make_engine() -> Engine:
    settings = get_settings()
    url = settings.database_url
    # Ensure the parent directory exists for file-based SQLite URLs.
    if url.startswith("sqlite:///"):
        db_path = Path(url.removeprefix("sqlite:///"))
        db_path.parent.mkdir(parents=True, exist_ok=True)
    return create_engine(url, future=True)


engine: Engine = _make_engine()
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, future=True)


def init_db() -> None:
    """Create all tables if they do not already exist. Idempotent."""
    Base.metadata.create_all(engine)


@contextmanager
def session_scope() -> Iterator[Session]:
    """Transactional session context: commit on success, roll back on error."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
