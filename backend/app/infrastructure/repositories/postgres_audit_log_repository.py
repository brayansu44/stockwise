from sqlalchemy.orm import Session

from app.domain.entities.audit_log import AuditLog
from app.domain.repositories.audit_log_repository import AuditLogRepository
from app.infrastructure.database.models.audit_log_model import AuditLogModel
from app.infrastructure.mappers.audit_log_mapper import AuditLogMapper


class PostgresAuditLogRepository(AuditLogRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_without_commit(
        self,
        audit_log: AuditLog,
    ) -> AuditLog:
        model = AuditLogMapper.entity_to_model(audit_log)

        self.db_session.add(model)
        self.db_session.flush()

        return AuditLogMapper.model_to_entity(model)