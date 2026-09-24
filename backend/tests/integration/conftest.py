from pathlib import Path

import pytest
from dotenv import dotenv_values
from sqlalchemy.engine import make_url

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

@pytest.fixture(scope="session")
def test_database_url():
    env_path = Path(__file__).resolve().parents[2] / ".env.test"

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

