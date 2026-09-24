from sqlalchemy.engine import make_url
from sqlalchemy import create_engine, text


def test_database_uses_test_environment(test_database_url):
    database_name = make_url(test_database_url).database

    assert database_name == "stockwise_test_db"

def test_database_connection(test_database_url):
    engine = create_engine(test_database_url)

    try:
        with engine.connect() as connection:
            database_name = connection.execute(
                text("SELECT current_database()")
            ).scalar_one()

            assert database_name == "stockwise_test_db"
    finally:
        engine.dispose()

