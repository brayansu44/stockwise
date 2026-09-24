from fastapi import status

from app.domain.entities.user import User
from app.domain.entities.user_role import UserRole
from app.domain.entities.category import Category
from app.domain.entities.product import Product

from app.infrastructure.repositories.postgres_user_repository import (
    PostgresUserRepository,
)
from app.infrastructure.security.jwt_token_service import JwtTokenService
from app.infrastructure.repositories.postgres_category_repository import (
    PostgresCategoryRepository,
)
from app.infrastructure.repositories.postgres_product_repository import (
    PostgresProductRepository,
)

def test_list_products_without_authentication(client):
    # Act
    response = client.get("/products/")

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_list_products_with_authentication(client, db_session):
    # Arrange
    user_repository = PostgresUserRepository(db_session)

    user = User(
        id=None,
        name="API Test User",
        email="api.products@test.com",
        hashed_password="test_password_hash",
        role=UserRole.ADMIN,
    )

    created_user = user_repository.create(user)

    token_service = JwtTokenService()
    token = token_service.create_access_token(
        subject=str(created_user.id)
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Act
    response = client.get(
        "/products/",
        headers=headers,
    )

    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_list_products_with_invalid_token(client):
    # Arrange
    headers = {
        "Authorization": "Bearer invalid_token"
    }

    # Act
    response = client.get(
        "/products/",
        headers=headers,
    )

    # Assert
    assert response.status_code == 401
    assert response.json()["detail"] == (
        "Invalid or expired token"
    )

def test_create_product_with_insufficient_permissions(
    client,
    db_session,
):
    # Arrange
    user_repository = PostgresUserRepository(db_session)

    user = User(
        id=None,
        name="Seller Test",
        email="seller.permissions@test.com",
        hashed_password="test_password_hash",
        role=UserRole.SELLER,
    )

    created_user = user_repository.create(user)

    token_service = JwtTokenService()
    token = token_service.create_access_token(
        subject=str(created_user.id)
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    product_data = {
        "name": "Test Product",
        "code": "TEST-001",
        "description": "Product for authorization testing",
        "price": 15000,
        "current_stock": 10,
        "minimum_stock": 2,
        "category_id": 1,
    }

    # Act
    response = client.post(
        "/products/",
        json=product_data,
        headers=headers,
    )

    # Assert
    assert response.status_code == 403

def test_create_product_as_admin(client, db_session):
    # Arrange: Create a test category
    category_repository = PostgresCategoryRepository(db_session)

    category = category_repository.create(
        Category(
            id=None,
            name="API Test Category",
            description="Category for API testing",
        )
    )

    # Arrange: Create an administrator
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="API Test Admin",
            email="admin.products@test.com",
            hashed_password="test_password_hash",
            role=UserRole.ADMIN,
        )
    )

    # Generate authentication token
    token_service = JwtTokenService()
    token = token_service.create_access_token(
        subject=str(admin.id)
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    product_data = {
        "name": "API Test Product",
        "code": "API-PROD-001",
        "description": "Product created through the API",
        "price": 25000,
        "current_stock": 15,
        "minimum_stock": 3,
        "category_id": category.id,
    }

    # Act
    response = client.post(
        "/products/",
        json=product_data,
        headers=headers,
    )

    # Assert
    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["name"] == product_data["name"]
    assert data["code"] == product_data["code"]
    assert data["category_id"] == category.id
    assert data["current_stock"] == 15

def test_get_product_by_code(client, db_session):
    # Arrange: Create a category
    category_repository = PostgresCategoryRepository(db_session)

    category = category_repository.create(
        Category(
            id=None,
            name="Product Lookup Category",
            description="Category for product lookup testing",
        )
    )

    # Arrange: Create a product
    product_repository = PostgresProductRepository(db_session)

    product = Product(
        id=None,
        name="Lookup Test Product",
        code="LOOKUP-001",
        description="Product for lookup testing",
        price=30000,
        current_stock=20,
        minimum_stock=5,
        category_id=category.id,
    )

    product_repository.create(product)

    # Act
    response = client.get("/products/LOOKUP-001")

    # Assert
    assert response.status_code == 200

    data = response.json()

    assert data["code"] == "LOOKUP-001"
    assert data["name"] == "Lookup Test Product"
    assert data["category_id"] == category.id

def test_get_product_by_code_not_found(client):
    # Act
    response = client.get(
        "/products/NONEXISTENT-PRODUCT-999999"
    )

    # Assert
    assert response.status_code == 404

def test_update_product_as_admin(client, db_session):
    # Arrange: Create a category
    category_repository = PostgresCategoryRepository(db_session)

    category = category_repository.create(
        Category(
            id=None,
            name="Update Test Category",
            description="Category for update testing",
        )
    )

    # Arrange: Create a product
    product_repository = PostgresProductRepository(db_session)

    product_repository.create(
        Product(
            id=None,
            name="Original Product",
            code="UPDATE-001",
            description="Original description",
            price=20000,
            current_stock=10,
            minimum_stock=2,
            category_id=category.id,
        )
    )

    # Arrange: Create an administrator
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="Update Test Admin",
            email="admin.update@test.com",
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

    update_data = {
        "name": "Updated Product",
        "price": 35000,
        "minimum_stock": 5,
    }

    # Act
    response = client.patch(
        "/products/UPDATE-001",
        json=update_data,
        headers=headers,
    )

    # Assert: Verify API response
    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Updated Product"
    assert data["price"] == 35000
    assert data["minimum_stock"] == 5
    assert data["current_stock"] == 10

    # Assert: Verify database changes
    updated_product = product_repository.get_by_code(
        "UPDATE-001"
    )

    assert updated_product is not None
    assert updated_product.name == "Updated Product"
    assert updated_product.price == 35000
    assert updated_product.minimum_stock == 5

def test_update_nonexistent_product(client, db_session):
    # Arrange: Create an administrator
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="Update Error Admin",
            email="admin.update.error@test.com",
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

    update_data = {
        "name": "Updated Product",
        "price": 35000,
    }

    # Act
    response = client.patch(
        "/products/NONEXISTENT-999999",
        json=update_data,
        headers=headers,
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Product not found"

def test_update_product_with_negative_price(client, db_session):
    # Arrange: Create an administrator
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="Validation Test Admin",
            email="admin.validation@test.com",
            hashed_password="test_password_hash",
            role=UserRole.ADMIN,
        )
    )

    # Generate authentication token
    token_service = JwtTokenService()

    token = token_service.create_access_token(
        subject=str(admin.id)
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    update_data = {
        "name": "Invalid Product",
        "price": -100,
    }

    # Act
    response = client.patch(
        "/products/INVALID-001",
        json=update_data,
        headers=headers,
    )

    # Assert
    assert response.status_code == 422
