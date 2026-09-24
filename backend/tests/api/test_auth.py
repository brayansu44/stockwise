from fastapi import status

from app.domain.entities.user import User
from app.domain.entities.user_role import UserRole
from app.infrastructure.repositories.postgres_user_repository import (
    PostgresUserRepository,
)
from app.infrastructure.security.password_hasher import (
    Argon2PasswordHasher,
)

def test_login_without_required_fields(client):
    # Act
    response = client.post(
        "/auth/login",
        json={},
    )

    # Assert
    assert response.status_code == (
        status.HTTP_422_UNPROCESSABLE_ENTITY
    )

    errors = response.json()["detail"]

    assert any(
        error["loc"][-1] == "email"
        for error in errors
    )

    assert any(
        error["loc"][-1] == "password"
        for error in errors
    )

def test_login_with_valid_credentials(client, db_session):
    # Arrange
    password = "SecurePassword123!"

    password_hasher = Argon2PasswordHasher()
    hashed_password = password_hasher.hash(password)

    user_repository = PostgresUserRepository(db_session)

    user = user_repository.create(
        User(
            id=None,
            name="Authentication Test",
            email="auth.valid@test.com",
            hashed_password=hashed_password,
            role=UserRole.ADMIN,
        )
    )

    # Act
    response = client.post(
        "/auth/login",
        json={
            "email": user.email,
            "password": password,
        },
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert "access_token" in data
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 0

def test_login_with_invalid_password(client, db_session):
    # Arrange
    password_hasher = Argon2PasswordHasher()

    user_repository = PostgresUserRepository(db_session)

    user = user_repository.create(
        User(
            id=None,
            name="Invalid Password Test",
            email="auth.invalid@test.com",
            hashed_password=password_hasher.hash(
                "CorrectPassword123!"
            ),
            role=UserRole.ADMIN,
        )
    )

    # Act
    response = client.post(
        "/auth/login",
        json={
            "email": user.email,
            "password": "WrongPassword123!",
        },
    )

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "access_token" not in response.json()

def test_login_with_nonexistent_email(client):
    # Act
    response = client.post(
        "/auth/login",
        json={
            "email": "nonexistent@test.com",
            "password": "SecurePassword123!",
        },
    )

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "access_token" not in response.json()

def test_login_with_inactive_user(client, db_session):
    # Arrange
    password = "SecurePassword123!"

    password_hasher = Argon2PasswordHasher()
    user_repository = PostgresUserRepository(db_session)

    user = user_repository.create(
        User(
            id=None,
            name="Inactive Authentication Test",
            email="auth.inactive@test.com",
            hashed_password=password_hasher.hash(password),
            role=UserRole.ADMIN,
            is_active=False,
        )
    )

    # Act
    response = client.post(
        "/auth/login",
        json={
            "email": user.email,
            "password": password,
        },
    )

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "User is inactive"
    assert "access_token" not in response.json()
