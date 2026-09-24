import pytest

import app.infrastructure.database.models

from app.application.dto.sale_dto import CreateSaleItemRequest
from app.application.use_cases.create_sale import CreateSaleUseCase

from app.domain.entities.category import Category
from app.domain.entities.product import Product
from app.domain.entities.user import User
from app.domain.entities.user_role import UserRole

from app.infrastructure.repositories.postgres_category_repository import (
    PostgresCategoryRepository,
)
from app.infrastructure.repositories.postgres_product_repository import (
    PostgresProductRepository,
)
from app.infrastructure.repositories.postgres_user_repository import (
    PostgresUserRepository,
)
from app.infrastructure.repositories.postgres_sale_repository import (
    PostgresSaleRepository,
)
from app.infrastructure.repositories.postgres_inventory_movement_repository import (
    PostgresInventoryMovementRepository,
)
from app.infrastructure.unit_of_work import SqlAlchemyUnitOfWork

from app.application.use_cases.cancel_sale import CancelSaleUseCase
from app.domain.entities.sale_status import SaleStatus

class FailingInventoryMovementRepository(
    PostgresInventoryMovementRepository
):
    def create_without_commit(self, movement):
        raise RuntimeError("Simulated sale transaction failure")

@pytest.fixture
def seller(db_session):
    user_repository = PostgresUserRepository(db_session)

    user = User(
        id=None,
        name="Integration Test Seller",
        email="seller.sale.integration@test.com",
        hashed_password="test_password_hash",
        role=UserRole.SELLER,
    )

    return user_repository.create(user)

@pytest.fixture
def sale_product(db_session):
    category_repository = PostgresCategoryRepository(db_session)
    product_repository = PostgresProductRepository(db_session)

    category = category_repository.create(
        Category(
            id=None,
            name="Sale Transaction Category",
            description="Category for sale integration testing",
        )
    )

    product = product_repository.create(
        Product(
            id=None,
            name="Gaming Keyboard",
            code="INT-SALE-001",
            description="Product for sale transaction testing",
            price=250000,
            current_stock=10,
            minimum_stock=2,
            category_id=category.id,
        )
    )

    return product

def test_sale_rollback_when_movement_creation_fails(
    db_session,
    seller,
    sale_product,
):
    # Arrange
    product_repository = PostgresProductRepository(db_session)
    sale_repository = PostgresSaleRepository(db_session)

    movement_repository = FailingInventoryMovementRepository(
        db_session
    )

    unit_of_work = SqlAlchemyUnitOfWork(db_session)

    use_case = CreateSaleUseCase(
        sale_repository=sale_repository,
        product_repository=product_repository,
        inventory_movement_repository=movement_repository,
        unit_of_work=unit_of_work,
    )

    # Act
    with pytest.raises(
        RuntimeError,
        match="Simulated sale transaction failure",
    ):
        use_case.execute(
            seller_id=seller.id,
            items=[
                CreateSaleItemRequest(
                    product_code=sale_product.code,
                    quantity=3,
                )
            ],
        )

    # Assert: product stock must remain unchanged
    db_session.expire_all()

    saved_product = product_repository.get_by_code(
        sale_product.code
    )

    assert saved_product is not None
    assert saved_product.current_stock == 10

    # Assert: no sale should remain in the database
    saved_sales = sale_repository.list_all()

    assert saved_sales == []

def test_sale_transaction_commits_successfully(
    db_session,
    seller,
    sale_product,
):
    # Arrange
    product_repository = PostgresProductRepository(db_session)
    sale_repository = PostgresSaleRepository(db_session)

    movement_repository = PostgresInventoryMovementRepository(
        db_session
    )

    unit_of_work = SqlAlchemyUnitOfWork(db_session)

    use_case = CreateSaleUseCase(
        sale_repository=sale_repository,
        product_repository=product_repository,
        inventory_movement_repository=movement_repository,
        unit_of_work=unit_of_work,
    )

    # Act
    sale = use_case.execute(
        seller_id=seller.id,
        items=[
            CreateSaleItemRequest(
                product_code=sale_product.code,
                quantity=3,
            )
        ],
    )

    # Assert
    db_session.expire_all()

    saved_product = product_repository.get_by_code(
        sale_product.code
    )

    saved_sale = sale_repository.get_by_id(sale.id)

    movements = movement_repository.list_by_product(
        sale_product.id
    )

    assert saved_product is not None
    assert saved_product.current_stock == 7

    assert saved_sale is not None
    assert saved_sale.seller_id == seller.id

    assert len(movements) == 1
    assert movements[0].quantity == 3
    assert movements[0].sale_id == sale.id

def test_cancel_sale_rollback_when_movement_creation_fails(
    db_session,
    seller,
    sale_product,
):
    product_repository = PostgresProductRepository(db_session)
    sale_repository = PostgresSaleRepository(db_session)
    movement_repository = PostgresInventoryMovementRepository(
        db_session
    )
    unit_of_work = SqlAlchemyUnitOfWork(db_session)

    # Create a valid sale first
    create_sale_use_case = CreateSaleUseCase(
        sale_repository=sale_repository,
        product_repository=product_repository,
        inventory_movement_repository=movement_repository,
        unit_of_work=unit_of_work,
    )

    sale = create_sale_use_case.execute(
        seller_id=seller.id,
        items=[
            CreateSaleItemRequest(
                product_code=sale_product.code,
                quantity=3,
            )
        ],
    )

    # Simulate a failure during cancellation
    failing_movement_repository = (
        FailingInventoryMovementRepository(db_session)
    )

    cancel_sale_use_case = CancelSaleUseCase(
        sale_repository=sale_repository,
        product_repository=product_repository,
        inventory_movement_repository=failing_movement_repository,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(
        RuntimeError,
        match="Simulated sale transaction failure",
    ):
        cancel_sale_use_case.execute(sale.id)

    # Reload persisted data after rollback
    db_session.expire_all()

    saved_product = product_repository.get_by_code(
        sale_product.code
    )
    saved_sale = sale_repository.get_by_id(sale.id)
    movements = movement_repository.list_by_product(
        sale_product.id
    )

    assert saved_product is not None
    assert saved_product.current_stock == 7

    assert saved_sale is not None
    assert saved_sale.status != SaleStatus.CANCELLED

    # Only the original sale movement should exist
    assert len(movements) == 1
