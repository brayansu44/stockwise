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

from app.domain.entities.audit_action import AuditAction
from app.domain.entities.audit_result import AuditResult
from app.infrastructure.database.models.audit_log_model import (
    AuditLogModel,
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

    # Verify user creation audit
    db_session.expire_all()

    audit_logs = db_session.query(AuditLogModel).filter(
        AuditLogModel.action == AuditAction.CREATE.value,
        AuditLogModel.entity_type == "user",
        AuditLogModel.entity_id == str(created_user.id),
    ).all()

    assert len(audit_logs) == 1

    audit_log = audit_logs[0]

    assert audit_log.user_id == admin.id
    assert audit_log.action == AuditAction.CREATE.value
    assert audit_log.entity_type == "user"
    assert audit_log.entity_id == str(created_user.id)
    assert audit_log.result == AuditResult.SUCCESS.value

    assert audit_log.old_values is None

    assert audit_log.new_values == {
        "name": "New Seller",
        "role": UserRole.SELLER.value,
        "is_active": True,
    }

    # Sensitive information must not be audited
    assert "password" not in audit_log.new_values
    assert "hashed_password" not in audit_log.new_values
    assert "email" not in audit_log.new_values

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

def test_get_users_as_admin(client, db_session):
    # Arrange
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="List Users Admin",
            email="admin.list.users@test.com",
            hashed_password="test_password_hash",
            role=UserRole.ADMIN,
        )
    )

    user_repository.create(
        User(
            id=None,
            name="List Users Seller",
            email="seller.list.users@test.com",
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

    # Act
    response = client.get(
        "/users/",
        headers=headers,
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    emails = [user["email"] for user in data]

    assert "admin.list.users@test.com" in emails
    assert "seller.list.users@test.com" in emails

def test_update_user_as_admin(client, db_session):
    # Arrange
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="Update User Admin",
            email="admin.update.user@test.com",
            hashed_password="test_password_hash",
            role=UserRole.ADMIN,
        )
    )

    user = user_repository.create(
        User(
            id=None,
            name="Original User",
            email="original.api@test.com",
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
        "name": "Updated User",
        "email": "updated.api@test.com",
        "role": UserRole.INVENTORY_OPERATOR.value,
    }

    # Act
    response = client.put(
        f"/users/{user.id}",
        json=payload,
        headers=headers,
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["id"] == user.id
    assert data["name"] == "Updated User"
    assert data["email"] == "updated.api@test.com"
    assert data["role"] == UserRole.INVENTORY_OPERATOR.value
    assert data["is_active"] is True

    # Verify user update audit
    db_session.expire_all()

    audit_logs = db_session.query(AuditLogModel).filter(
        AuditLogModel.action == AuditAction.UPDATE.value,
        AuditLogModel.entity_type == "user",
        AuditLogModel.entity_id == str(user.id),
    ).all()

    assert len(audit_logs) == 1

    audit_log = audit_logs[0]

    assert audit_log.user_id == admin.id
    assert audit_log.action == AuditAction.UPDATE.value
    assert audit_log.entity_type == "user"
    assert audit_log.entity_id == str(user.id)
    assert audit_log.result == AuditResult.SUCCESS.value

    assert audit_log.old_values == {
        "name": "Original User",
        "role": UserRole.SELLER.value,
    }

    assert audit_log.new_values == {
        "name": "Updated User",
        "role": UserRole.INVENTORY_OPERATOR.value,
    }

    # Sensitive information must not be audited
    for values in (
        audit_log.old_values,
        audit_log.new_values,
    ):
        assert "password" not in values
        assert "hashed_password" not in values
        assert "email" not in values

def test_update_user_not_found(client, db_session):
    # Arrange
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="Update Not Found Admin",
            email="admin.update.notfound@test.com",
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
        "name": "Nonexistent User",
        "email": "nonexistent.update@test.com",
        "role": UserRole.SELLER.value,
    }

    # Act
    response = client.put(
        "/users/999999999",
        json=payload,
        headers=headers,
    )

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "User not found"

def test_deactivate_user_as_admin(client, db_session):
    # Arrange
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="Deactivate User Admin",
            email="admin.deactivate@test.com",
            hashed_password="test_password_hash",
            role=UserRole.ADMIN,
        )
    )

    user = user_repository.create(
        User(
            id=None,
            name="User To Deactivate",
            email="user.deactivate@test.com",
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

    # Act
    response = client.patch(
        f"/users/{user.id}/deactivate",
        headers=headers,
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["id"] == user.id
    assert data["is_active"] is False

        # Verify user deactivation audit
    db_session.expire_all()

    audit_logs = db_session.query(AuditLogModel).filter(
        AuditLogModel.action == AuditAction.DEACTIVATE.value,
        AuditLogModel.entity_type == "user",
        AuditLogModel.entity_id == str(user.id),
    ).all()

    assert len(audit_logs) == 1

    audit_log = audit_logs[0]

    assert audit_log.user_id == admin.id
    assert audit_log.action == AuditAction.DEACTIVATE.value
    assert audit_log.entity_type == "user"
    assert audit_log.entity_id == str(user.id)
    assert audit_log.result == AuditResult.SUCCESS.value

    assert audit_log.old_values == {
        "is_active": True,
    }

    assert audit_log.new_values == {
        "is_active": False,
    }

def test_activate_user_as_admin(client, db_session):
    # Arrange
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="Activate User Admin",
            email="admin.activate@test.com",
            hashed_password="test_password_hash",
            role=UserRole.ADMIN,
        )
    )

    user = user_repository.create(
        User(
            id=None,
            name="User To Activate",
            email="user.activate@test.com",
            hashed_password="test_password_hash",
            role=UserRole.SELLER,
            is_active=False,
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
        f"/users/{user.id}/activate",
        headers=headers,
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["id"] == user.id
    assert data["is_active"] is True

        # Verify user activation audit
    db_session.expire_all()

    audit_logs = db_session.query(AuditLogModel).filter(
        AuditLogModel.action == AuditAction.ACTIVATE.value,
        AuditLogModel.entity_type == "user",
        AuditLogModel.entity_id == str(user.id),
    ).all()

    assert len(audit_logs) == 1

    audit_log = audit_logs[0]

    assert audit_log.user_id == admin.id
    assert audit_log.action == AuditAction.ACTIVATE.value
    assert audit_log.entity_type == "user"
    assert audit_log.entity_id == str(user.id)
    assert audit_log.result == AuditResult.SUCCESS.value

    assert audit_log.old_values == {
        "is_active": False,
    }

    assert audit_log.new_values == {
        "is_active": True,
    }

def test_deactivate_user_not_found(client, db_session):
    # Arrange
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="Deactivate Not Found Admin",
            email="admin.deactivate.notfound@test.com",
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
        "/users/999999999/deactivate",
        headers=headers,
    )

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "User not found"

def test_activate_user_not_found(client, db_session):
    # Arrange
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="Activate Not Found Admin",
            email="admin.activate.notfound@test.com",
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
        "/users/999999999/activate",
        headers=headers,
    )

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "User not found"
