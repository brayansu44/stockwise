import pytest

from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import IntegrityError

from app.domain.entities.category import Category
from app.domain.entities.product import Product

from app.infrastructure.repositories.postgres_category_repository import (
    PostgresCategoryRepository,
)

from app.infrastructure.repositories.postgres_product_repository import (
    PostgresProductRepository,
)

def test_create_product_with_category(db_session):
    # Arrange
    category_repository = PostgresCategoryRepository(db_session)
    product_repository = PostgresProductRepository(db_session)

    category = category_repository.create(
        Category(
            id=None,
            name="Integration Peripherals",
            description="Computer peripherals",
        )
    )

    product = Product(
        id=None,
        name="Mechanical Keyboard",
        code="INT-KB-001",
        description="Mechanical keyboard for integration testing",
        price=250000,
        current_stock=10,
        minimum_stock=3,
        category_id=category.id,
    )

    # Act
    created_product = product_repository.create(product)

    # Assert
    assert created_product.id is not None
    assert created_product.code == "INT-KB-001"
    assert created_product.category_id == category.id

    # Verify persisted data
    saved_product = product_repository.get_by_code("INT-KB-001")

    assert saved_product is not None
    assert saved_product.id == created_product.id
    assert saved_product.category_id == category.id
    assert saved_product.current_stock == 10

def test_create_product_with_nonexistent_category(db_session):
    # Arrange
    repository = PostgresProductRepository(db_session)

    product = Product(
        id=None,
        name="Invalid Keyboard",
        code="INT-INVALID-001",
        description="Product with nonexistent category",
        price=150000,
        current_stock=10,
        minimum_stock=3,
        category_id=999999,
    )

    # Act & Assert
    with pytest.raises(IntegrityError):
        repository.create(product)

def test_product_category_cannot_be_null(db_session):
    # Arrange
    insert_statement = text("""
        INSERT INTO products (
            name,
            code,
            description,
            price,
            current_stock,
            minimum_stock,
            category_id,
            is_active
        )
        VALUES (
            'Invalid Product',
            'INT-NULL-001',
            'Product without category',
            100000,
            10,
            2,
            NULL,
            TRUE
        )
    """)

    # Act & Assert
    with pytest.raises(IntegrityError):
        db_session.execute(insert_statement)
        db_session.flush()

def test_update_product(db_session):
    # Arrange
    category_repository = PostgresCategoryRepository(db_session)
    product_repository = PostgresProductRepository(db_session)

    category = category_repository.create(
        Category(
            id=None,
            name="Update Test Category",
            description="Category for product updates",
        )
    )

    product = product_repository.create(
        Product(
            id=None,
            name="Mechanical Keyboard",
            code="INT-UPDATE-001",
            description="Original description",
            price=250000,
            current_stock=10,
            minimum_stock=3,
            category_id=category.id,
        )
    )

    # Act
    product.name = "Gaming Keyboard"
    product.price = 300000
    product.minimum_stock = 5

    updated_product = product_repository.update(product)

    # Assert
    assert updated_product.name == "Gaming Keyboard"
    assert updated_product.price == 300000
    assert updated_product.minimum_stock == 5

    # Verify persisted data
    saved_product = product_repository.get_by_code(
        "INT-UPDATE-001"
    )

    assert saved_product is not None
    assert saved_product.name == "Gaming Keyboard"
    assert saved_product.price == 300000
    assert saved_product.minimum_stock == 5
    assert saved_product.category_id == category.id

def test_update_product_category(db_session):
    # Arrange
    category_repository = PostgresCategoryRepository(db_session)
    product_repository = PostgresProductRepository(db_session)

    original_category = category_repository.create(
        Category(
            id=None,
            name="Keyboards",
            description="Keyboard products",
        )
    )

    new_category = category_repository.create(
        Category(
            id=None,
            name="Gaming Accessories",
            description="Gaming products",
        )
    )

    product = product_repository.create(
        Product(
            id=None,
            name="Gaming Keyboard",
            code="INT-CATEGORY-001",
            description="Gaming mechanical keyboard",
            price=300000,
            current_stock=10,
            minimum_stock=3,
            category_id=original_category.id,
        )
    )

    # Act
    product.category_id = new_category.id

    updated_product = product_repository.update(product)

    # Assert
    assert updated_product.category_id == new_category.id

    saved_product = product_repository.get_by_code(
        "INT-CATEGORY-001"
    )

    assert saved_product is not None
    assert saved_product.category_id == new_category.id
    assert saved_product.category_id != original_category.id

def test_update_product_without_commit(db_session):
    # Arrange
    category_repository = PostgresCategoryRepository(db_session)
    product_repository = PostgresProductRepository(db_session)

    category = category_repository.create(
        Category(
            id=None,
            name="Transaction Test Category",
            description="Category for transaction testing",
        )
    )

    product = product_repository.create(
        Product(
            id=None,
            name="Wireless Mouse",
            code="INT-TRANSACTION-001",
            description="Mouse for transaction testing",
            price=120000,
            current_stock=10,
            minimum_stock=3,
            category_id=category.id,
        )
    )

    # Act
    product.current_stock = 7

    updated_product = product_repository.update_without_commit(
        product
    )

    # Assert
    assert updated_product.current_stock == 7

    saved_product = product_repository.get_by_id(product.id)

    assert saved_product is not None
    assert saved_product.current_stock == 7

def test_product_stock_rollback_with_two_connections(
    test_database_url,
):
    # Safety check
    database_name = make_url(test_database_url).database

    if database_name != "stockwise_test_db":
        raise RuntimeError("Unsafe test database configuration")

    engine = create_engine(test_database_url)

    try:
        # Create test records and commit them.
        with engine.begin() as connection:
            category_id = connection.execute(
                text("""
                    INSERT INTO categories (
                        name,
                        description,
                        is_active
                    )
                    VALUES (
                        'Rollback Test Category',
                        'Transaction testing',
                        TRUE
                    )
                    RETURNING id
                """)
            ).scalar_one()

            product_id = connection.execute(
                text("""
                    INSERT INTO products (
                        name,
                        code,
                        description,
                        price,
                        current_stock,
                        minimum_stock,
                        category_id,
                        is_active
                    )
                    VALUES (
                        'Rollback Mouse',
                        'INT-ROLLBACK-001',
                        'Transaction testing',
                        120000,
                        10,
                        3,
                        :category_id,
                        TRUE
                    )
                    RETURNING id
                """),
                {"category_id": category_id},
            ).scalar_one()

        try:
            # First connection: update without committing.
            with engine.connect() as connection:
                transaction = connection.begin()

                try:
                    connection.execute(
                        text("""
                            UPDATE products
                            SET current_stock = 7
                            WHERE id = :product_id
                        """),
                        {"product_id": product_id},
                    )

                    # First connection sees its own changes.
                    stock = connection.execute(
                        text("""
                            SELECT current_stock
                            FROM products
                            WHERE id = :product_id
                        """),
                        {"product_id": product_id},
                    ).scalar_one()

                    assert stock == 7

                    # Second connection sees committed data.
                    with engine.connect() as second_connection:
                        stock = second_connection.execute(
                            text("""
                                SELECT current_stock
                                FROM products
                                WHERE id = :product_id
                            """),
                            {"product_id": product_id},
                        ).scalar_one()

                        assert stock == 10

                finally:
                    transaction.rollback()

            # Verify the original stock after rollback.
            with engine.connect() as connection:
                stock = connection.execute(
                    text("""
                        SELECT current_stock
                        FROM products
                        WHERE id = :product_id
                    """),
                    {"product_id": product_id},
                ).scalar_one()

                assert stock == 10

        finally:
            # Clean up test records.
            with engine.begin() as connection:
                connection.execute(
                    text("""
                        DELETE FROM products
                        WHERE id = :product_id
                    """),
                    {"product_id": product_id},
                )

                connection.execute(
                    text("""
                        DELETE FROM categories
                        WHERE id = :category_id
                    """),
                    {"category_id": category_id},
                )

    finally:
        engine.dispose()

def test_update_nonexistent_product(db_session):
    repository = PostgresProductRepository(db_session)

    product = Product(
        id=999999,
        name="Nonexistent Product",
        code="MISSING-001",
        description="Product that does not exist",
        price=25000,
        current_stock=10,
        minimum_stock=2,
        category_id=999999,
    )

    with pytest.raises(ValueError, match="Product not found"):
        repository.update(product)

def test_update_without_commit_nonexistent_product(db_session):
    repository = PostgresProductRepository(db_session)

    product = Product(
        id=999999,
        name="Nonexistent Product",
        code="MISSING-002",
        description="Product that does not exist",
        price=25000,
        current_stock=10,
        minimum_stock=2,
        category_id=999999,
    )

    with pytest.raises(ValueError, match="Product not found"):
        repository.update_without_commit(product)

def test_get_nonexistent_product_by_id(db_session):
    repository = PostgresProductRepository(db_session)

    product = repository.get_by_id(999999)

    assert product is None
