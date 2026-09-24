import pytest

import app.infrastructure.database.models

from app.domain.entities.sale import Sale
from app.domain.entities.sale_item import SaleItem
from app.domain.entities.category import Category
from app.domain.entities.product import Product
from app.domain.entities.user import User
from app.domain.entities.user_role import UserRole
from app.domain.entities.sale_status import SaleStatus

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

@pytest.fixture
def seller(db_session):
    user_repository = PostgresUserRepository(db_session)

    return user_repository.create(
        User(
            id=None,
            name="Sale Repository Test Seller",
            email="seller.repository@test.com",
            hashed_password="test_password_hash",
            role=UserRole.SELLER,
        )
    )


@pytest.fixture
def sale_product(db_session):
    category_repository = PostgresCategoryRepository(db_session)
    product_repository = PostgresProductRepository(db_session)

    category = category_repository.create(
        Category(
            id=None,
            name="Sale Repository Category",
            description="Category for repository testing",
        )
    )

    return product_repository.create(
        Product(
            id=None,
            name="Gaming Mouse",
            code="INT-SALE-REPO-001",
            description="Product for sale repository testing",
            price=150000,
            current_stock=10,
            minimum_stock=2,
            category_id=category.id,
        )
    )

def test_create_sale_successfully(
    db_session,
    seller,
    sale_product,
):
    # Arrange
    sale_repository = PostgresSaleRepository(db_session)

    sale = Sale(
        id=None,
        seller_id=seller.id,
        items=[
            SaleItem(
                product_id=sale_product.id,
                quantity=2,
                unit_price=sale_product.price,
            )
        ],
    )

    # Act
    created_sale = sale_repository.create(sale)

    # Assert
    saved_sale = sale_repository.get_by_id(created_sale.id)

    assert created_sale.id is not None
    assert saved_sale is not None
    assert saved_sale.seller_id == seller.id

    assert len(saved_sale.items) == 1
    assert saved_sale.items[0].product_id == sale_product.id
    assert saved_sale.items[0].quantity == 2
    assert saved_sale.items[0].unit_price == 150000
    assert saved_sale.total == 300000

def test_list_sales_successfully(
    db_session,
    seller,
    sale_product,
):
    # Arrange
    sale_repository = PostgresSaleRepository(db_session)

    sale = Sale(
        id=None,
        seller_id=seller.id,
        items=[
            SaleItem(
                product_id=sale_product.id,
                quantity=2,
                unit_price=sale_product.price,
            )
        ],
    )

    created_sale = sale_repository.create(sale)

    # Act
    sales = sale_repository.list_all()

    # Assert
    assert len(sales) == 1
    assert sales[0].id == created_sale.id
    assert sales[0].seller_id == seller.id
    assert len(sales[0].items) == 1
    assert sales[0].items[0].quantity == 2
    assert sales[0].total == 300000

def test_update_sale_status_successfully(
    db_session,
    seller,
    sale_product,
):
    # Arrange
    sale_repository = PostgresSaleRepository(db_session)

    sale = Sale(
        id=None,
        seller_id=seller.id,
        items=[
            SaleItem(
                product_id=sale_product.id,
                quantity=2,
                unit_price=sale_product.price,
            )
        ],
    )

    created_sale = sale_repository.create(sale)

    # Act
    created_sale.status = SaleStatus.CANCELLED

    sale_repository.update_without_commit(created_sale)
    db_session.commit()

    # Assert
    db_session.expire_all()

    saved_sale = sale_repository.get_by_id(created_sale.id)

    assert saved_sale is not None
    assert saved_sale.status == SaleStatus.CANCELLED

def test_get_sale_by_id_not_found(db_session):
    # Arrange
    sale_repository = PostgresSaleRepository(db_session)

    # Act
    sale = sale_repository.get_by_id(999999)

    # Assert
    assert sale is None

def test_update_sale_not_found(db_session):
    # Arrange
    sale_repository = PostgresSaleRepository(db_session)

    sale = Sale(
        id=999999,
        seller_id=1,
        items=[],
    )

    # Act & Assert
    with pytest.raises(ValueError, match="Sale not found"):
        sale_repository.update_without_commit(sale)


