import pytest
import app.infrastructure.database.models

from app.domain.entities.category import Category
from app.domain.entities.product import Product
from app.domain.entities.movement_type import MovementType

from app.application.use_cases.create_inventory_movement import (
    CreateInventoryMovementUseCase,
)

from app.infrastructure.repositories.postgres_category_repository import (
    PostgresCategoryRepository,
)

from app.infrastructure.repositories.postgres_product_repository import (
    PostgresProductRepository,
)

from app.infrastructure.repositories.postgres_inventory_movement_repository import (
    PostgresInventoryMovementRepository,
)

from app.infrastructure.unit_of_work import SqlAlchemyUnitOfWork



class FailingInventoryMovementRepository(
    PostgresInventoryMovementRepository
):
    def create_without_commit(self, movement):
        raise RuntimeError("Simulated database failure")

def test_inventory_rollback_when_movement_creation_fails(
    db_session,
):
    # Arrange
    category_repository = PostgresCategoryRepository(db_session)
    product_repository = PostgresProductRepository(db_session)

    movement_repository = FailingInventoryMovementRepository(
        db_session
    )

    unit_of_work = SqlAlchemyUnitOfWork(db_session)

    category = category_repository.create(
        Category(
            id=None,
            name="Inventory Rollback Category",
            description="Transaction rollback testing",
        )
    )

    product = product_repository.create(
        Product(
            id=None,
            name="Rollback Keyboard",
            code="INT-ROLLBACK-INV-001",
            description="Inventory rollback testing",
            price=200000,
            current_stock=10,
            minimum_stock=2,
            category_id=category.id,
        )
    )

    use_case = CreateInventoryMovementUseCase(
        inventory_movement_repository=movement_repository,
        product_repository=product_repository,
        unit_of_work=unit_of_work,
    )

    # Act: simulate an error while creating the movement.
    with pytest.raises(
        RuntimeError,
        match="Simulated database failure",
    ):
        use_case.execute(
            product_code=product.code,
            movement_type=MovementType.EXIT,
            quantity=3,
            reason="Rollback integration test",
        )

    # Assert: the stock must remain unchanged.
    saved_product = product_repository.get_by_code(
        product.code
    )

    assert saved_product is not None
    assert saved_product.current_stock == 10

def test_inventory_exit_commits_successfully(db_session):
    # Arrange
    category_repository = PostgresCategoryRepository(db_session)
    product_repository = PostgresProductRepository(db_session)
    movement_repository = PostgresInventoryMovementRepository(
        db_session
    )
    unit_of_work = SqlAlchemyUnitOfWork(db_session)

    category = category_repository.create(
        Category(
            id=None,
            name="Inventory Success Category",
            description="Successful transaction testing",
        )
    )

    product = product_repository.create(
        Product(
            id=None,
            name="Wireless Keyboard",
            code="INT-SUCCESS-INV-001",
            description="Successful inventory transaction",
            price=180000,
            current_stock=10,
            minimum_stock=2,
            category_id=category.id,
        )
    )

    use_case = CreateInventoryMovementUseCase(
        inventory_movement_repository=movement_repository,
        product_repository=product_repository,
        unit_of_work=unit_of_work,
    )

    # Act
    movement = use_case.execute(
        product_code=product.code,
        movement_type=MovementType.EXIT,
        quantity=3,
        reason="Successful integration test",
    )

    # Assert
    saved_product = product_repository.get_by_code(product.code)
    saved_movements = movement_repository.list_by_product(
        product.id
    )

    assert saved_product is not None
    assert saved_product.current_stock == 7

    assert movement.id is not None
    assert movement.quantity == 3
    assert movement.movement_type == MovementType.EXIT

    assert len(saved_movements) == 1
    assert saved_movements[0].id == movement.id
    assert saved_movements[0].product_id == product.id


