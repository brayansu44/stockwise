from app.domain.entities.audit_log import AuditLog
from app.domain.repositories.audit_log_repository import (
    AuditLogRepository,
)


class FakeAuditLogRepository(AuditLogRepository):
    def __init__(self):
        self.audit_logs: list[AuditLog] = []

    def create_without_commit(
        self,
        audit_log: AuditLog,
    ) -> AuditLog:
        audit_log.id = len(self.audit_logs) + 1
        self.audit_logs.append(audit_log)

        return audit_log