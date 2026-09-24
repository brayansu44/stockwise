from unittest.mock import MagicMock

import pytest

from app.infrastructure.repositories.postgres_sale_repository import (
    PostgresSaleRepository,
)

from app.domain.entities.sale import Sale
from app.domain.entities.sale_status import SaleStatus


def test_commit_rolls_back_on_database_error():
    db_session = MagicMock()

    db_session.commit.side_effect = RuntimeError(
        "Database commit failed"
    )

    repository = PostgresSaleRepository(db_session)

    with pytest.raises(
        RuntimeError,
        match="Database commit failed",
    ):
        repository.commit()

    db_session.commit.assert_called_once()
    db_session.rollback.assert_called_once()

def test_create_rolls_back_on_database_error():
    db_session = MagicMock()

    db_session.flush.side_effect = RuntimeError(
        "Database flush failed"
    )

    repository = PostgresSaleRepository(db_session)

    sale = Sale(
        id=None,
        seller_id=1,
        items=[],
        status=SaleStatus.COMPLETED,
    )

    with pytest.raises(
        RuntimeError,
        match="Database flush failed",
    ):
        repository.create(sale)

    db_session.rollback.assert_called_once()
    db_session.commit.assert_not_called()
