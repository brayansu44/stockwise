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

def test_get_all_users_successfully(db_session):
    # Arrange
    user_repository = PostgresUserRepository(db_session)

    first_user = User(
        id=None,
        name="First User",
        email="first.repository@test.com",
        hashed_password="test_password_hash",
        role=UserRole.ADMIN,
    )

    second_user = User(
        id=None,
        name="Second User",
        email="second.repository@test.com",
        hashed_password="test_password_hash",
        role=UserRole.SELLER,
    )

    first_created_user = user_repository.create(first_user)
    second_created_user = user_repository.create(second_user)

    # Act
    users = user_repository.get_all()

    # Assert
    user_ids = [user.id for user in users]

    assert first_created_user.id in user_ids
    assert second_created_user.id in user_ids

def test_update_user_successfully(db_session):
    # Arrange
    user_repository = PostgresUserRepository(db_session)

    user = User(
        id=None,
        name="Original User",
        email="original.repository@test.com",
        hashed_password="original_password_hash",
        role=UserRole.SELLER,
    )

    created_user = user_repository.create(user)

    created_user.name = "Updated User"
    created_user.email = "updated.repository@test.com"
    created_user.hashed_password = "updated_password_hash"
    created_user.role = UserRole.INVENTORY_OPERATOR
    created_user.is_active = False

    # Act
    updated_user = user_repository.update(created_user)

    # Assert
    assert updated_user.id == created_user.id
    assert updated_user.name == "Updated User"
    assert updated_user.email == "updated.repository@test.com"
    assert updated_user.hashed_password == "updated_password_hash"
    assert updated_user.role == UserRole.INVENTORY_OPERATOR
    assert updated_user.is_active is False

def test_update_user_not_found(db_session):
    # Arrange
    user_repository = PostgresUserRepository(db_session)

    user = User(
        id=999999999,
        name="Nonexistent User",
        email="nonexistent.repository@test.com",
        hashed_password="test_password_hash",
        role=UserRole.SELLER,
    )

    # Act / Assert
    with pytest.raises(
        ValueError,
        match="User not found",
    ):
        user_repository.update(user)
