from fastapi import status

from app.domain.entities.user import User
from app.domain.entities.user_role import UserRole
from app.infrastructure.repositories.postgres_user_repository import (
    PostgresUserRepository,
)
from app.infrastructure.security.jwt_token_service import JwtTokenService

from app.domain.entities.category import Category
from app.domain.entities.product import Product
from app.infrastructure.repositories.postgres_category_repository import (
    PostgresCategoryRepository,
)
from app.infrastructure.repositories.postgres_product_repository import (
    PostgresProductRepository,
)

def test_create_inventory_movement_without_authentication(client):
    movement_data = {
        "product_code": "TEST-001",
        "movement_type": "ENTRY",
        "quantity": 5,
        "reason": "Initial stock",
    }

    response = client.post(
        "/inventory-movements/",
        json=movement_data,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_create_inventory_movement_with_nonexistent_product(
    client,
    db_session,
):
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="Inventory Test Admin",
            email="admin.inventory@test.com",
            hashed_password="test_password_hash",
            role=UserRole.ADMIN,
        )
    )

    token_service = JwtTokenService()
    token = token_service.create_access_token(
        subject=str(admin.id)
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    movement_data = {
        "product_code": "NONEXISTENT-999",
        "movement_type": "entry",
        "quantity": 5,
        "reason": "Initial stock",
    }

    response = client.post(
        "/inventory-movements/",
        json=movement_data,
        headers=headers,
    )

    assert response.status_code == 400

def test_create_inventory_entry_as_admin(client, db_session):
    # Create category
    category_repository = PostgresCategoryRepository(db_session)

    category = category_repository.create(
        Category(
            id=None,
            name="Inventory Entry Category",
            description="Category for inventory testing",
        )
    )

    # Create product
    product_repository = PostgresProductRepository(db_session)

    product = product_repository.create(
        Product(
            id=None,
            name="Gaming Mouse",
            code="INV-ENTRY-001",
            description="Mouse for inventory testing",
            price=120000,
            current_stock=10,
            minimum_stock=2,
            category_id=category.id,
        )
    )

    # Create administrator
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="Inventory Entry Admin",
            email="admin.inventory.entry@test.com",
            hashed_password="test_password_hash",
            role=UserRole.ADMIN,
        )
    )

    token = JwtTokenService().create_access_token(
        subject=str(admin.id)
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Register inventory entry
    response = client.post(
        "/inventory-movements/",
        json={
            "product_code": product.code,
            "movement_type": "entry",
            "quantity": 5,
            "reason": "Inventory replenishment",
        },
        headers=headers,
    )

    assert response.status_code == 201

    # Verify updated stock
    db_session.expire_all()

    updated_product = product_repository.get_by_code(
        product.code
    )

    assert updated_product is not None
    assert updated_product.current_stock == 15

    # Verify API response
    data = response.json()

    assert data["product_id"] == product.id
    assert data["quantity"] == 5
    assert data["movement_type"] == "entry"

def test_list_inventory_movements_by_product_as_admin(
    client,
    db_session,
):
    category_repository = PostgresCategoryRepository(db_session)
    product_repository = PostgresProductRepository(db_session)
    user_repository = PostgresUserRepository(db_session)

    category = category_repository.create(
        Category(
            id=None,
            name="Movement History Category",
            description="Category for movement history testing",
        )
    )

    product = product_repository.create(
        Product(
            id=None,
            name="Gaming Headset",
            code="INV-HISTORY-001",
            description="Headset for movement history testing",
            price=180000,
            current_stock=10,
            minimum_stock=2,
            category_id=category.id,
        )
    )

    admin = user_repository.create(
        User(
            id=None,
            name="Movement History Admin",
            email="admin.inventory.history@test.com",
            hashed_password="test_password_hash",
            role=UserRole.ADMIN,
        )
    )

    token = JwtTokenService().create_access_token(
        subject=str(admin.id)
    )

    headers = {"Authorization": f"Bearer {token}"}

    # Create a movement
    create_response = client.post(
        "/inventory-movements/",
        json={
            "product_code": product.code,
            "movement_type": "entry",
            "quantity": 5,
            "reason": "Inventory replenishment",
        },
        headers=headers,
    )

    assert create_response.status_code == 201

    # Retrieve movement history
    response = client.get(
        f"/inventory-movements/product/{product.code}",
        headers=headers,
    )

    assert response.status_code == 200

    movements = response.json()

    assert len(movements) == 1
    assert movements[0]["product_id"] == product.id
    assert movements[0]["quantity"] == 5
    assert movements[0]["movement_type"] == "entry"

def test_seller_cannot_create_inventory_movement(
    client,
    db_session,
):
    user_repository = PostgresUserRepository(db_session)

    seller = user_repository.create(
        User(
            id=None,
            name="Inventory Test Seller",
            email="seller.inventory@test.com",
            hashed_password="test_password_hash",
            role=UserRole.SELLER,
        )
    )

    token = JwtTokenService().create_access_token(
        subject=str(seller.id)
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.post(
        "/inventory-movements/",
        json={
            "product_code": "TEST-001",
            "movement_type": "entry",
            "quantity": 5,
            "reason": "Unauthorized inventory entry",
        },
        headers=headers,
    )

    assert response.status_code == 403

def test_seller_can_list_inventory_movements(
    client,
    db_session,
):
    user_repository = PostgresUserRepository(db_session)

    seller = user_repository.create(
        User(
            id=None,
            name="Inventory History Seller",
            email="seller.inventory.history@test.com",
            hashed_password="test_password_hash",
            role=UserRole.SELLER,
        )
    )

    token = JwtTokenService().create_access_token(
        subject=str(seller.id)
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.get(
        "/inventory-movements/product/NONEXISTENT-999",
        headers=headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

def test_inventory_operator_can_create_movement(
    client,
    db_session,
):
    category_repository = PostgresCategoryRepository(db_session)
    product_repository = PostgresProductRepository(db_session)
    user_repository = PostgresUserRepository(db_session)

    category = category_repository.create(
        Category(
            id=None,
            name="Operator Test Category",
            description="Inventory operator testing",
        )
    )

    product = product_repository.create(
        Product(
            id=None,
            name="Wireless Mouse",
            code="INV-OP-001",
            description="Operator test product",
            price=95000,
            current_stock=10,
            minimum_stock=2,
            category_id=category.id,
        )
    )

    operator = user_repository.create(
        User(
            id=None,
            name="Inventory Operator",
            email="inventory.operator@test.com",
            hashed_password="test_password_hash",
            role=UserRole.INVENTORY_OPERATOR,
        )
    )

    token = JwtTokenService().create_access_token(
        subject=str(operator.id)
    )

    response = client.post(
        "/inventory-movements/",
        json={
            "product_code": product.code,
            "movement_type": "entry",
            "quantity": 5,
            "reason": "Stock replenishment",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201

    db_session.expire_all()

    updated_product = product_repository.get_by_code(
        product.code
    )

    assert updated_product is not None
    assert updated_product.current_stock == 15
