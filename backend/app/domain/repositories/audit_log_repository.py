from abc import ABC, abstractmethod

from app.domain.entities.audit_log import AuditLog


class AuditLogRepository(ABC):
    @abstractmethod
    def create_without_commit(self, audit_log: AuditLog) -> AuditLog:
        pass