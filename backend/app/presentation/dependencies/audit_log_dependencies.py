from fastapi import Depends
from sqlalchemy.orm import Session

from app.infrastructure.repositories.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)
from app.presentation.dependencies.database_dependencies import get_db_session


def get_audit_log_repository(
    db_session: Session = Depends(get_db_session),
) -> PostgresAuditLogRepository:
    return PostgresAuditLogRepository(db_session)