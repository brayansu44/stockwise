from unittest.mock import MagicMock, patch

import pytest

from app.presentation.dependencies.database_dependencies import (
    get_db_session,
)


def test_get_db_session_closes_session():
    mock_session = MagicMock()

    with patch(
        "app.presentation.dependencies.database_dependencies.SessionLocal",
        return_value=mock_session,
    ):
        session_generator = get_db_session()

        session = next(session_generator)

        assert session is mock_session

        with pytest.raises(StopIteration):
            next(session_generator)

        mock_session.close.assert_called_once()

def test_get_db_session_closes_session_on_error():
    mock_session = MagicMock()

    with patch(
        "app.presentation.dependencies.database_dependencies.SessionLocal",
        return_value=mock_session,
    ):
        session_generator = get_db_session()

        session = next(session_generator)

        assert session is mock_session

        with pytest.raises(RuntimeError, match="Database operation failed"):
            session_generator.throw(
                RuntimeError("Database operation failed")
            )

        mock_session.close.assert_called_once()
