"""Test configuration and fixtures for Data Contracts Studio Backend.

This module provides shared test fixtures and configuration for the test suite.
"""

import os
import pytest
import tempfile
from app.core.database import Base, get_db
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from typing import Generator


@pytest.fixture(scope="session")
def test_db_engine():
    """Create a test database engine for the session.

    Yields:
        SQLAlchemy engine for testing.
    """
    # Create temporary database file
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    database_url = f"sqlite:///{db_path}"

    engine = create_engine(database_url, connect_args={"check_same_thread": False})

    # Create all tables
    Base.metadata.create_all(bind=engine)

    yield engine

    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope="function")
def test_db_session(test_db_engine) -> Generator[Session, None, None]:
    """Create a database session for each test.

    Args:
        test_db_engine: Test database engine fixture.

    Yields:
        Database session for testing.
    """
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_db_engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(test_db_session: Session) -> Generator[TestClient, None, None]:
    """Create a test client with database dependency override.

    Args:
        test_db_session: Test database session fixture.

    Yields:
        FastAPI test client.
    """

    def override_get_db() -> Generator[Session, None, None]:
        """Override database dependency for testing."""
        try:
            yield test_db_session
        finally:
            pass  # Session cleanup handled by test_db_session fixture

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    # Clean up dependency override
    app.dependency_overrides.clear()


@pytest.fixture
def mock_contract_data() -> dict:
    """Provide sample contract data for testing.

    Returns:
        Dictionary with sample contract data.
    """
    return {
        "name": "test_contract",
        "version": "1.0.0",
        "description": "A test data contract",
        "schema": {
            "type": "object",
            "properties": {
                "user_id": {"type": "integer"},
                "email": {"type": "string"},
                "created_at": {"type": "string", "format": "date-time"},
            },
            "required": ["user_id", "email"],
        },
    }


# Configure pytest markers
pytest_plugins = []
