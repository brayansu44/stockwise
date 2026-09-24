from fastapi import status

from app.domain.entities.user import User
from app.domain.entities.user_role import UserRole
from app.infrastructure.repositories.postgres_user_repository import (
    PostgresUserRepository,
)
from app.infrastructure.security.jwt_token_service import (
    JwtTokenService,
)
from app.infrastructure.security.password_hasher import (
    Argon2PasswordHasher,
)

def test_create_user_without_authentication(client):
    # Arrange
    payload = {
        "name": "Test User",
        "email": "test.user@example.com",
        "password": "SecurePassword123!",
        "role": "SELLER",
    }

    # Act
    response = client.post(
        "/users/",
        json=payload,
    )

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_create_user_as_admin(client, db_session):
    # Arrange: Create an administrator
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="Test Administrator",
            email="admin.create@test.com",
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
        "name": "New Seller",
        "email": "new.seller@test.com",
        "password": "SecurePassword123!",
        "role": UserRole.SELLER.value,
    }

    # Act
    response = client.post(
        "/users/",
        json=payload,
        headers=headers,
    )
    
    # Assert: Verify HTTP response
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert "hashed_password" not in data
    assert "password" not in data

    # Verify database persistence
    created_user = user_repository.get_by_email(
        payload["email"]
    )

    assert created_user is not None
    assert created_user.role == UserRole.SELLER

    # Verify password hashing
    password_hasher = Argon2PasswordHasher()

    assert created_user.hashed_password != payload["password"]

    assert password_hasher.verify(
        payload["password"],
        created_user.hashed_password,
    )

def test_create_user_as_seller_forbidden(client, db_session):
    # Arrange: Create a seller
    user_repository = PostgresUserRepository(db_session)

    seller = user_repository.create(
        User(
            id=None,
            name="Test Seller",
            email="seller.permissions@test.com",
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
        "name": "Unauthorized User",
        "email": "unauthorized@test.com",
        "password": "SecurePassword123!",
        "role": "SELLER",
    }

    # Act
    response = client.post(
        "/users/",
        json=payload,
        headers=headers,
    )

    # Assert
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Verify that no user was created
    created_user = user_repository.get_by_email(
        payload["email"]
    )

    assert created_user is None

def test_create_user_with_duplicate_email(client, db_session):
    # Arrange
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="Test Administrator",
            email="admin.duplicate@test.com",
            hashed_password="test_password_hash",
            role=UserRole.ADMIN,
        )
    )

    existing_user = user_repository.create(
        User(
            id=None,
            name="Existing User",
            email="duplicate@test.com",
            hashed_password="test_password_hash",
            role=UserRole.SELLER,
        )
    )

    token = JwtTokenService().create_access_token(
        subject=str(admin.id)
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    payload = {
        "name": "Another User",
        "email": existing_user.email,
        "password": "SecurePassword123!",
        "role": UserRole.SELLER.value,
    }

    # Act
    response = client.post(
        "/users/",
        json=payload,
        headers=headers,
    )

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "User email already exists"

def test_create_user_with_short_password(client, db_session):
    # Arrange
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="Password Test Admin",
            email="admin.password@test.com",
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
        "name": "Short Password User",
        "email": "short.password@test.com",
        "password": "123",
        "role": UserRole.SELLER.value,
    }

    # Act
    response = client.post(
        "/users/",
        json=payload,
        headers=headers,
    )

    # Assert
    assert response.status_code in (
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    )

    # Verify that the user was not created
    created_user = user_repository.get_by_email(
        payload["email"]
    )

    assert created_user is None
