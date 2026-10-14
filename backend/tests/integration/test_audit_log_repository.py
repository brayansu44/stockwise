from app.domain.entities.audit_action import AuditAction
from app.domain.entities.audit_log import AuditLog
from app.domain.entities.audit_result import AuditResult
from app.infrastructure.repositories.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def test_create_audit_log_without_commit(db_session):
    # Arrange
    repository = PostgresAuditLogRepository(db_session)

    audit_log = AuditLog(
        id=None,
        user_id=None,
        action=AuditAction.LOGIN_FAILURE,
        entity_type="auth",
        entity_id=None,
        old_values=None,
        new_values={
            "email": "test@example.com",
        },
        result=AuditResult.FAILURE,
    )

    audit_log.validate()

    # Act
    created_audit_log = repository.create_without_commit(
        audit_log
    )

    # Assert
    assert created_audit_log.id is not None
    assert created_audit_log.user_id is None
    assert created_audit_log.action == AuditAction.LOGIN_FAILURE
    assert created_audit_log.entity_type == "auth"
    assert created_audit_log.entity_id is None
    assert created_audit_log.old_values is None
    assert created_audit_log.new_values == {
        "email": "test@example.com",
    }
    assert created_audit_log.result == AuditResult.FAILURE
    assert created_audit_log.created_at is not None

    assert db_session.in_transaction() is True