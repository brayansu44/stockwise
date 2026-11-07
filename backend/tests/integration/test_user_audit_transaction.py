import pytest

import app.infrastructure.database.models

from app.application.use_cases.create_user import CreateUserUseCase
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
from app.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from app.application.use_cases.update_user import UpdateUserUseCase
from app.application.use_cases.change_user_status import (
    ChangeUserStatusUseCase,
)

class FailingUserAuditRepository(PostgresAuditLogRepository):
    def create_without_commit(self, audit_log):
        super().create_without_commit(audit_log)

        raise RuntimeError(
            "Simulated user audit failure"
        )


def test_create_user_rollback_when_audit_creation_fails(
    db_session,
):
    # Arrange
    user_repository = PostgresUserRepository(db_session)
    audit_log_repository = FailingUserAuditRepository(db_session)
    password_hasher = Argon2PasswordHasher()
    unit_of_work = SqlAlchemyUnitOfWork(db_session)

    use_case = CreateUserUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
        audit_log_repository=audit_log_repository,
        unit_of_work=unit_of_work,
    )

    user = User(
        id=None,
        name="Rollback Seller",
        email="rollback.seller@test.com",
        hashed_password="",
        role=UserRole.SELLER,
    )

    # Act
    with pytest.raises(
        RuntimeError,
        match="Simulated user audit failure",
    ):
        use_case.execute(
            user=user,
            plain_password="SecurePassword123!",
            created_by_user_id=1,
        )

    # Assert
    db_session.expire_all()

    saved_user = user_repository.get_by_email(
        "rollback.seller@test.com"
    )

    assert saved_user is None

    audit_logs = db_session.query(AuditLogModel).filter(
        AuditLogModel.action == AuditAction.CREATE.value,
        AuditLogModel.entity_type == "user",
        AuditLogModel.new_values["name"].as_string()
        == "Rollback Seller",
    ).all()

    assert audit_logs == []

def test_update_user_rollback_when_audit_creation_fails(
    db_session,
):
    # Arrange
    user_repository = PostgresUserRepository(db_session)
    audit_log_repository = FailingUserAuditRepository(db_session)
    unit_of_work = SqlAlchemyUnitOfWork(db_session)

    user = user_repository.create(
        User(
            id=None,
            name="Original User",
            email="original.rollback@test.com",
            hashed_password="test_password_hash",
            role=UserRole.SELLER,
        )
    )

    use_case = UpdateUserUseCase(
        user_repository=user_repository,
        audit_log_repository=audit_log_repository,
        unit_of_work=unit_of_work,
    )

    # Act
    with pytest.raises(
        RuntimeError,
        match="Simulated user audit failure",
    ):
        use_case.execute(
            user_id=user.id,
            name="Updated User",
            email="updated.rollback@test.com",
            role=UserRole.INVENTORY_OPERATOR,
            updated_by_user_id=1,
        )

    # Reload persisted data after rollback
    db_session.expire_all()

    saved_user = user_repository.get_by_id(user.id)

    # Assert: user changes were rolled back
    assert saved_user is not None
    assert saved_user.name == "Original User"
    assert saved_user.email == "original.rollback@test.com"
    assert saved_user.role == UserRole.SELLER

    audit_logs = db_session.query(AuditLogModel).filter(
        AuditLogModel.action == AuditAction.UPDATE.value,
        AuditLogModel.entity_type == "user",
        AuditLogModel.entity_id == str(user.id),
    ).all()

    assert audit_logs == []

def test_deactivate_user_rollback_when_audit_creation_fails(
    db_session,
):
    # Arrange
    user_repository = PostgresUserRepository(db_session)
    audit_log_repository = FailingUserAuditRepository(db_session)
    unit_of_work = SqlAlchemyUnitOfWork(db_session)

    user = user_repository.create(
        User(
            id=None,
            name="Deactivation Rollback User",
            email="deactivation.rollback@test.com",
            hashed_password="test_password_hash",
            role=UserRole.SELLER,
            is_active=True,
        )
    )

    use_case = ChangeUserStatusUseCase(
        user_repository=user_repository,
        audit_log_repository=audit_log_repository,
        unit_of_work=unit_of_work,
    )

    # Act
    with pytest.raises(
        RuntimeError,
        match="Simulated user audit failure",
    ):
        use_case.execute(
            user_id=user.id,
            is_active=False,
            changed_by_user_id=1,
        )

    # Reload database state after rollback
    db_session.expire_all()

    saved_user = user_repository.get_by_id(user.id)

    # Assert
    assert saved_user is not None
    assert saved_user.is_active is True

    audit_logs = db_session.query(AuditLogModel).filter(
        AuditLogModel.action == AuditAction.DEACTIVATE.value,
        AuditLogModel.entity_type == "user",
        AuditLogModel.entity_id == str(user.id),
    ).all()

    assert audit_logs == []

def test_activate_user_rollback_when_audit_creation_fails(
    db_session,
):
    # Arrange
    user_repository = PostgresUserRepository(db_session)
    audit_log_repository = FailingUserAuditRepository(db_session)
    unit_of_work = SqlAlchemyUnitOfWork(db_session)

    user = user_repository.create(
        User(
            id=None,
            name="Activation Rollback User",
            email="activation.rollback@test.com",
            hashed_password="test_password_hash",
            role=UserRole.SELLER,
            is_active=False,
        )
    )

    use_case = ChangeUserStatusUseCase(
        user_repository=user_repository,
        audit_log_repository=audit_log_repository,
        unit_of_work=unit_of_work,
    )

    # Act
    with pytest.raises(
        RuntimeError,
        match="Simulated user audit failure",
    ):
        use_case.execute(
            user_id=user.id,
            is_active=True,
            changed_by_user_id=1,
        )

    # Reload database state after rollback
    db_session.expire_all()

    saved_user = user_repository.get_by_id(user.id)

    # Assert
    assert saved_user is not None
    assert saved_user.is_active is False

    audit_logs = db_session.query(AuditLogModel).filter(
        AuditLogModel.action == AuditAction.ACTIVATE.value,
        AuditLogModel.entity_type == "user",
        AuditLogModel.entity_id == str(user.id),
    ).all()

    assert audit_logs == []
