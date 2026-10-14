from app.domain.entities.audit_action import AuditAction
from app.domain.entities.audit_log import AuditLog
from app.domain.entities.audit_result import AuditResult
from app.infrastructure.database.models.audit_log_model import AuditLogModel


class AuditLogMapper:
    @staticmethod
    def model_to_entity(model: AuditLogModel) -> AuditLog:
        return AuditLog(
            id=model.id,
            user_id=model.user_id,
            action=AuditAction(model.action),
            entity_type=model.entity_type,
            entity_id=model.entity_id,
            old_values=model.old_values,
            new_values=model.new_values,
            result=AuditResult(model.result),
            created_at=model.created_at,
        )

    @staticmethod
    def entity_to_model(entity: AuditLog) -> AuditLogModel:
        return AuditLogModel(
            user_id=entity.user_id,
            action=entity.action.value,
            entity_type=entity.entity_type,
            entity_id=entity.entity_id,
            old_values=entity.old_values,
            new_values=entity.new_values,
            result=entity.result.value,
        )