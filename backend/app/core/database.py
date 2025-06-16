"""Database configuration and session management.

This module provides database connectivity, session management, and dependency
injection for the Data Contracts Studio application using SQLAlchemy.
"""

from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from typing import Generator


def create_database_engine() -> Engine:
    """Create and configure the database engine.

    Returns:
        Engine: Configured SQLAlchemy engine instance.
    """
    connect_args = {}
    if "sqlite" in settings.database_url:
        connect_args["check_same_thread"] = False

    return create_engine(settings.database_url, connect_args=connect_args)


# Database engine and session configuration
engine = create_database_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Dependency injection for database sessions.

    This function provides a database session with automatic cleanup.
    Used as a FastAPI dependency to ensure proper session management.

    Yields:
        Session: SQLAlchemy database session.

    Example:
        @app.get("/contracts/")
        def get_contracts(db: Session = Depends(get_db)):
            return db.query(Contract).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
