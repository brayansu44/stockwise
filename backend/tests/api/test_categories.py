from fastapi import status

from app.domain.entities.user import User
from app.domain.entities.user_role import UserRole
from app.domain.entities.category import Category

from app.infrastructure.repositories.postgres_user_repository import (
    PostgresUserRepository,
)
from app.infrastructure.security.jwt_token_service import (
    JwtTokenService,
)
from app.infrastructure.repositories.postgres_category_repository import (
    PostgresCategoryRepository,
)

def test_list_categories_without_authentication(client):
    # Act
    response = client.get("/categories/")

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_list_categories_with_authentication(client, db_session):
    # Arrange: Create a test user
    user_repository = PostgresUserRepository(db_session)

    user = user_repository.create(
        User(
            id=None,
            name="Category Test User",
            email="category.list@test.com",
            hashed_password="test_password_hash",
            role=UserRole.ADMIN,
        )
    )

    # Generate JWT
    token_service = JwtTokenService()

    token = token_service.create_access_token(
        subject=str(user.id)
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Act
    response = client.get(
        "/categories/",
        headers=headers,
    )

    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_category_as_admin(client, db_session):
    # Arrange
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="Category Admin",
            email="category.admin@test.com",
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

    payload = {
        "name": "Electronics",
        "description": "Electronic products",
    }

    # Act
    response = client.post(
        "/categories/",
        json=payload,
        headers=headers,
    )

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "Electronics"
    assert response.json()["description"] == "Electronic products"

    # Verify database persistence
    category_repository = PostgresCategoryRepository(db_session)

    category = category_repository.get_by_name("Electronics")

    assert category is not None
    assert category.name == "Electronics"

def test_create_category_as_seller_forbidden(client, db_session):
    # Arrange
    user_repository = PostgresUserRepository(db_session)

    seller = user_repository.create(
        User(
            id=None,
            name="Category Seller",
            email="category.seller@test.com",
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

    payload = {
        "name": "Furniture",
        "description": "Furniture products",
    }

    # Act
    response = client.post(
        "/categories/",
        json=payload,
        headers=headers,
    )

    # Assert
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Verify that the category was not created
    category_repository = PostgresCategoryRepository(db_session)

    category = category_repository.get_by_name("Furniture")

    assert category is None

def test_get_category_by_id(client, db_session):
    # Arrange: Create a category
    category_repository = PostgresCategoryRepository(db_session)

    category = category_repository.create(
        Category(
            id=None,
            name="Computers",
            description="Computer equipment",
        )
    )

    # Create an authenticated user
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="Category Reader",
            email="category.reader@test.com",
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

    # Act
    response = client.get(
        f"/categories/{category.id}",
        headers=headers,
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == category.id
    assert response.json()["name"] == "Computers"
    assert response.json()["description"] == "Computer equipment"

def test_get_nonexistent_category(client, db_session):
    # Arrange: Create an authenticated user
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="Category Not Found Test",
            email="category.notfound@test.com",
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

    # Act: Request a nonexistent category
    response = client.get(
        "/categories/999999",
        headers=headers,
    )

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_category_as_admin(client, db_session):
    # Arrange: Create a category
    category_repository = PostgresCategoryRepository(db_session)

    category = category_repository.create(
        Category(
            id=None,
            name="Old Category",
            description="Old description",
        )
    )

    # Create an administrator
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="Category Update Admin",
            email="category.update@test.com",
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

    payload = {
        "name": "Updated Category",
        "description": "Updated description",
    }

    # Act
    response = client.patch(
        f"/categories/{category.id}",
        json=payload,
        headers=headers,
    )

    # Assert: Verify HTTP response
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Updated Category"
    assert response.json()["description"] == "Updated description"

    # Verify database persistence
    updated_category = category_repository.get_by_id(category.id)

    assert updated_category is not None
    assert updated_category.name == "Updated Category"
    assert updated_category.description == "Updated description"

def test_update_nonexistent_category(client, db_session):
    # Arrange
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="Category Missing Admin",
            email="category.missing@test.com",
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

    payload = {
        "name": "Updated Category",
        "description": "Updated description",
    }

    # Act
    response = client.patch(
        "/categories/999999",
        json=payload,
        headers=headers,
    )

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_deactivate_category_as_admin(client, db_session):
    # Arrange: Create an active category
    category_repository = PostgresCategoryRepository(db_session)

    category = category_repository.create(
        Category(
            id=None,
            name="Inactive Test Category",
            description="Category to deactivate",
        )
    )

    # Create an administrator
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="Category Status Admin",
            email="category.status@test.com",
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

    # Act
    response = client.patch(
        f"/categories/{category.id}/deactivate",
        headers=headers,
    )

    # Assert: Verify HTTP response
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["is_active"] is False

    # Verify database persistence
    updated_category = category_repository.get_by_id(
        category.id
    )

    assert updated_category is not None
    assert updated_category.is_active is False

def test_activate_category_as_admin(client, db_session):
    # Arrange: Create an inactive category
    category_repository = PostgresCategoryRepository(db_session)

    category = category_repository.create(
        Category(
            id=None,
            name="Activation Test Category",
            description="Category to activate",
            is_active=False,
        )
    )

    # Create an administrator
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="Category Activation Admin",
            email="category.activation@test.com",
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

    # Act
    response = client.patch(
        f"/categories/{category.id}/activate",
        headers=headers,
    )

    # Assert: Verify HTTP response
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["is_active"] is True

    # Verify database persistence
    updated_category = category_repository.get_by_id(
        category.id
    )

    assert updated_category is not None
    assert updated_category.is_active is True

def test_deactivate_nonexistent_category(client, db_session):
    # Arrange
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="Category Missing Status Admin",
            email="category.missing.status@test.com",
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

    # Act
    response = client.patch(
        "/categories/999999/deactivate",
        headers=headers,
    )

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_category_as_seller_forbidden(client, db_session):
    # Arrange: Create a category
    category_repository = PostgresCategoryRepository(db_session)

    category = category_repository.create(
        Category(
            id=None,
            name="Protected Category",
            description="Original description",
        )
    )

    # Create a seller
    user_repository = PostgresUserRepository(db_session)

    seller = user_repository.create(
        User(
            id=None,
            name="Category Seller Update",
            email="category.seller.update@test.com",
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

    payload = {
        "name": "Modified Category",
        "description": "Modified description",
    }

    # Act
    response = client.patch(
        f"/categories/{category.id}",
        json=payload,
        headers=headers,
    )

    # Assert
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Verify that the original category remains unchanged
    saved_category = category_repository.get_by_id(category.id)

    assert saved_category.name == "Protected Category"
    assert saved_category.description == "Original description"
