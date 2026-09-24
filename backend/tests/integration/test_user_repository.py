import pytest

import app.infrastructure.database.models

from app.domain.entities.user import User
from app.domain.entities.user_role import UserRole

from app.infrastructure.repositories.postgres_user_repository import (
    PostgresUserRepository,
)

def test_create_user_successfully(db_session):
    # Arrange
    user_repository = PostgresUserRepository(db_session)

    user = User(
        id=None,
        name="Test User",
        email="user.repository@test.com",
        hashed_password="test_password_hash",
        role=UserRole.SELLER,
    )

    # Act
    created_user = user_repository.create(user)

    # Assert
    assert created_user.id is not None
    assert created_user.name == "Test User"
    assert created_user.email == "user.repository@test.com"
    assert created_user.role == UserRole.SELLER
    assert created_user.is_active is True

def test_get_user_by_email_successfully(db_session):
    # Arrange
    user_repository = PostgresUserRepository(db_session)

    user = User(
        id=None,
        name="Email Test User",
        email="email.test@test.com",
        hashed_password="test_password_hash",
        role=UserRole.SELLER,
    )

    created_user = user_repository.create(user)

    # Act
    found_user = user_repository.get_by_email(
        created_user.email
    )

    # Assert
    assert found_user is not None
    assert found_user.id == created_user.id
    assert found_user.name == created_user.name
    assert found_user.email == created_user.email
    assert found_user.role == UserRole.SELLER


def test_get_user_by_id_successfully(db_session):
    # Arrange
    user_repository = PostgresUserRepository(db_session)

    user = User(
        id=None,
        name="ID Test User",
        email="id.test@test.com",
        hashed_password="test_password_hash",
        role=UserRole.SELLER,
    )

    created_user = user_repository.create(user)

    # Act
    found_user = user_repository.get_by_id(created_user.id)

    # Assert
    assert found_user is not None
    assert found_user.id == created_user.id
    assert found_user.name == created_user.name
    assert found_user.email == created_user.email
    assert found_user.role == UserRole.SELLER

def test_get_user_by_email_not_found(db_session):
    # Arrange
    user_repository = PostgresUserRepository(db_session)

    # Act
    found_user = user_repository.get_by_email(
        "nonexistent@test.com"
    )

    # Assert
    assert found_user is None


def test_get_user_by_id_not_found(db_session):
    # Arrange
    user_repository = PostgresUserRepository(db_session)

    # Act
    found_user = user_repository.get_by_id(999999999)

    # Assert
    assert found_user is None
