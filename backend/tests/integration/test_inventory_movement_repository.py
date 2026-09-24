import pytest

from sqlalchemy.exc import IntegrityError

import app.infrastructure.database.models

from app.domain.entities.category import Category
from app.domain.entities.product import Product
from app.domain.entities.inventory_movement import InventoryMovement
from app.domain.entities.movement_type import MovementType

from app.infrastructure.repositories.postgres_category_repository import (
    PostgresCategoryRepository,
)
from app.infrastructure.repositories.postgres_product_repository import (
    PostgresProductRepository,
)
from app.infrastructure.repositories.postgres_inventory_movement_repository import (
    PostgresInventoryMovementRepository,
)

@pytest.fixture
def product(db_session):
    category_repository = PostgresCategoryRepository(db_session)
    product_repository = PostgresProductRepository(db_session)

    category = category_repository.create(
        Category(
            id=None,
            name="Inventory Movement Test Category",
            description="Category for inventory repository tests",
        )
    )

    return product_repository.create(
        Product(
            id=None,
            name="Mechanical Keyboard",
            code="INT-INV-REPO-001",
            description="Product for inventory movement tests",
            price=200000,
            current_stock=10,
            minimum_stock=2,
            category_id=category.id,
        )
    )

def test_create_inventory_movement_successfully(
    db_session,
    product,
):
    # Arrange
    movement_repository = PostgresInventoryMovementRepository(
        db_session
    )

    movement = InventoryMovement(
        id=None,
        product_id=product.id,
        movement_type=MovementType.ENTRY,
        quantity=5,
        reason="Inventory repository integration test",
    )

    # Act
    created_movement = movement_repository.create(movement)

    # Assert
    saved_movements = movement_repository.list_by_product(
        product.id
    )

    assert created_movement.id is not None
    assert created_movement.product_id == product.id
    assert created_movement.quantity == 5
    assert created_movement.movement_type == MovementType.ENTRY

    assert len(saved_movements) == 1
    assert saved_movements[0].id == created_movement.id
    assert saved_movements[0].quantity == 5

def test_create_inventory_movement_rolls_back_on_error(
    db_session,
):
    # Arrange
    movement_repository = PostgresInventoryMovementRepository(
        db_session
    )

    movement = InventoryMovement(
        id=None,
        product_id=999999999,
        movement_type=MovementType.ENTRY,
        quantity=5,
        reason="Testing repository rollback",
    )

    # Act
    with pytest.raises(IntegrityError):
        movement_repository.create(movement)

    # Assert
    assert db_session.in_transaction() is False
