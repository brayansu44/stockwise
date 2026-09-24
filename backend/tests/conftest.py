from pathlib import Path

import pytest

from dotenv import dotenv_values
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

from app.main import app
from app.presentation.dependencies.database_dependencies import (
    get_db_session,
)


@pytest.fixture(scope="session")
def test_database_url():
    env_path = Path(__file__).resolve().parents[1] / ".env.test"

    if not env_path.is_file():
        raise RuntimeError("Test environment file not found")

    config = dotenv_values(env_path)
    database_url = config.get("DATABASE_URL")

    if not database_url:
        raise RuntimeError("Test DATABASE_URL is not configured")

    database_name = make_url(database_url).database

    if database_name != "stockwise_test_db":
        raise RuntimeError(
            "Unsafe database configuration: expected stockwise_test_db"
        )

    return database_url


@pytest.fixture
def db_session(test_database_url):
    engine = create_engine(test_database_url)

    connection = engine.connect()
    transaction = connection.begin()

    session = Session(
        bind=connection,
        join_transaction_mode="create_savepoint",
    )

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()
        engine.dispose()


@pytest.fixture
def client(db_session):
    def override_get_db_session():
        yield db_session

    app.dependency_overrides[get_db_session] = (
        override_get_db_session
    )

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(
            get_db_session,
            None,
        )