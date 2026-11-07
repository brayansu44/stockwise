from fastapi import status

from app.domain.entities.user import User
from app.domain.entities.user_role import UserRole
from app.infrastructure.repositories.postgres_user_repository import (
    PostgresUserRepository,
)
from app.infrastructure.security.password_hasher import (
    Argon2PasswordHasher,
)

from app.domain.entities.audit_action import AuditAction
from app.domain.entities.audit_result import AuditResult
from app.infrastructure.database.models.audit_log_model import (
    AuditLogModel,
)

from fastapi.testclient import TestClient

from app.infrastructure.repositories.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)
from app.presentation.dependencies.audit_log_dependencies import (
    get_audit_log_repository,
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

    # Verify successful login audit
    db_session.expire_all()

    audit_logs = db_session.query(AuditLogModel).filter(
        AuditLogModel.user_id == user.id,
        AuditLogModel.action == AuditAction.LOGIN_SUCCESS.value,
    ).all()

    assert len(audit_logs) == 1

    audit_log = audit_logs[0]

    assert audit_log.user_id == user.id
    assert audit_log.action == AuditAction.LOGIN_SUCCESS.value
    assert audit_log.entity_type == "authentication"
    assert audit_log.entity_id == str(user.id)
    assert audit_log.result == AuditResult.SUCCESS.value

    assert audit_log.old_values is None
    assert audit_log.new_values is None

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

    # Verify failed login audit
    db_session.expire_all()

    audit_logs = db_session.query(AuditLogModel).filter(
        AuditLogModel.user_id == user.id,
        AuditLogModel.action == AuditAction.LOGIN_FAILURE.value,
    ).all()

    assert len(audit_logs) == 1

    audit_log = audit_logs[0]

    assert audit_log.user_id == user.id
    assert audit_log.action == AuditAction.LOGIN_FAILURE.value
    assert audit_log.entity_type == "authentication"
    assert audit_log.entity_id == str(user.id)
    assert audit_log.result == AuditResult.FAILURE.value

    assert audit_log.old_values is None
    assert audit_log.new_values is None

def test_login_with_nonexistent_email(client, db_session):
    # Arrange
    failed_audit_query = db_session.query(
        AuditLogModel
    ).filter(
        AuditLogModel.action == AuditAction.LOGIN_FAILURE.value,
        AuditLogModel.user_id.is_(None),
        AuditLogModel.entity_type == "authentication",
    )

    initial_count = failed_audit_query.count()

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

    # Verify failed login audit
    db_session.expire_all()

    assert failed_audit_query.count() == initial_count + 1

    audit_log = failed_audit_query.order_by(
        AuditLogModel.id.desc()
    ).first()

    assert audit_log is not None

    assert audit_log.user_id is None
    assert audit_log.entity_id is None
    assert audit_log.action == AuditAction.LOGIN_FAILURE.value
    assert audit_log.entity_type == "authentication"
    assert audit_log.result == AuditResult.FAILURE.value

    assert audit_log.old_values is None
    assert audit_log.new_values is None

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
    assert response.json()["detail"] == "Invalid email or password"
    assert "access_token" not in response.json()

    # Verify failed login audit for inactive user
    db_session.expire_all()

    audit_logs = db_session.query(AuditLogModel).filter(
        AuditLogModel.user_id == user.id,
        AuditLogModel.action == AuditAction.LOGIN_FAILURE.value,
    ).all()

    assert len(audit_logs) == 1

    audit_log = audit_logs[0]

    assert audit_log.user_id == user.id
    assert audit_log.action == AuditAction.LOGIN_FAILURE.value
    assert audit_log.entity_type == "authentication"
    assert audit_log.entity_id == str(user.id)
    assert audit_log.result == AuditResult.FAILURE.value

    assert audit_log.old_values is None
    assert audit_log.new_values is None

def test_login_audit_error_returns_internal_server_error(
    client,
    db_session,
):
    # Arrange
    class FailingAuditLogRepository(
        PostgresAuditLogRepository
    ):
        def create_without_commit(self, audit_log):
            raise ValueError(
                "Simulated audit persistence failure"
            )

    def override_audit_log_repository():
        return FailingAuditLogRepository(db_session)

    app = client.app

    previous_override = app.dependency_overrides.get(
        get_audit_log_repository
    )

    app.dependency_overrides[
        get_audit_log_repository
    ] = override_audit_log_repository

    try:
        # Act
        with TestClient(
            app,
            raise_server_exceptions=False,
        ) as test_client:
            response = test_client.post(
                "/auth/login",
                json={
                    "email": "audit.internal.error@example.com",
                    "password": "WrongPassword123!",
                },
            )

        # Assert
        assert response.status_code == (
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )

        assert (
            "Simulated audit persistence failure"
            not in response.text
        )

    finally:
        if previous_override is None:
            app.dependency_overrides.pop(
                get_audit_log_repository,
                None,
            )
        else:
            app.dependency_overrides[
                get_audit_log_repository
            ] = previous_override
