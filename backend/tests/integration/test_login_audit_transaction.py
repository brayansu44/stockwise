import pytest

import app.infrastructure.database.models

from app.application.use_cases.login_user import LoginUserUseCase

from app.domain.entities.audit_action import AuditAction
from app.domain.entities.user import User
from app.domain.entities.user_role import UserRole

from app.infrastructure.database.models.audit_log_model import (
    AuditLogModel,
)
from app.infrastructure.repositories.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)
from app.infrastructure.repositories.postgres_user_repository import (
    PostgresUserRepository,
)
from app.infrastructure.security.password_hasher import (
    Argon2PasswordHasher,
)
from app.infrastructure.security.jwt_token_service import (
    JwtTokenService,
)
from app.infrastructure.unit_of_work import SqlAlchemyUnitOfWork


class FailingLoginAuditRepository(PostgresAuditLogRepository):
    def create_without_commit(self, audit_log):
        super().create_without_commit(audit_log)

        raise RuntimeError("Simulated login audit failure")


def test_login_success_rollback_when_audit_creation_fails(
    db_session,
):
    # Arrange
    password = "SecurePassword123!"

    password_hasher = Argon2PasswordHasher()
    user_repository = PostgresUserRepository(db_session)

    user = user_repository.create(
        User(
            id=None,
            name="Login Audit Rollback Test",
            email="login.audit.rollback@test.com",
            hashed_password=password_hasher.hash(password),
            role=UserRole.ADMIN,
        )
    )

    audit_log_repository = FailingLoginAuditRepository(
        db_session
    )

    unit_of_work = SqlAlchemyUnitOfWork(db_session)

    use_case = LoginUserUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
        token_service=JwtTokenService(),
        audit_log_repository=audit_log_repository,
        unit_of_work=unit_of_work,
    )

    # Act
    with pytest.raises(
        RuntimeError,
        match="Simulated login audit failure",
    ):
        use_case.execute(
            email=user.email,
            password=password,
        )

    # Assert
    db_session.expire_all()

    audit_logs = db_session.query(AuditLogModel).filter(
        AuditLogModel.user_id == user.id,
        AuditLogModel.action == AuditAction.LOGIN_SUCCESS.value,
    ).all()

    assert audit_logs == []

    saved_user = user_repository.get_by_email(user.email)

    assert saved_user is not None
    assert saved_user.id == user.id

def test_login_failure_rollback_when_audit_creation_fails(
    db_session,
):
    # Arrange
    password_hasher = Argon2PasswordHasher()
    user_repository = PostgresUserRepository(db_session)

    user = user_repository.create(
        User(
            id=None,
            name="Failed Login Audit Rollback Test",
            email="login.failure.rollback@test.com",
            hashed_password=password_hasher.hash(
                "CorrectPassword123!"
            ),
            role=UserRole.ADMIN,
        )
    )

    audit_log_repository = FailingLoginAuditRepository(
        db_session
    )

    unit_of_work = SqlAlchemyUnitOfWork(db_session)

    use_case = LoginUserUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
        token_service=JwtTokenService(),
        audit_log_repository=audit_log_repository,
        unit_of_work=unit_of_work,
    )

    # Act
    with pytest.raises(
        RuntimeError,
        match="Simulated login audit failure",
    ):
        use_case.execute(
            email=user.email,
            password="WrongPassword123!",
        )

    # Assert
    db_session.expire_all()

    audit_logs = db_session.query(AuditLogModel).filter(
        AuditLogModel.user_id == user.id,
        AuditLogModel.action == AuditAction.LOGIN_FAILURE.value,
    ).all()

    assert audit_logs == []

    saved_user = user_repository.get_by_email(
        user.email
    )

    assert saved_user is not None
    assert saved_user.id == user.id
    assert saved_user.is_active is True
