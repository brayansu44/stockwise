from datetime import datetime, timezone

from app.domain.entities.audit_action import AuditAction
from app.domain.entities.audit_log import AuditLog
from app.domain.entities.audit_result import AuditResult
from app.infrastructure.database.models.audit_log_model import AuditLogModel
from app.infrastructure.mappers.audit_log_mapper import AuditLogMapper


def test_entity_to_model():
    audit_log = AuditLog(
        id=None,
        user_id=1,
        action=AuditAction.UPDATE,
        entity_type="product",
        entity_id="10",
        old_values={"name": "Old name"},
        new_values={"name": "New name"},
        result=AuditResult.SUCCESS,
    )

    model = AuditLogMapper.entity_to_model(audit_log)

    assert isinstance(model, AuditLogModel)
    assert model.user_id == 1
    assert model.action == AuditAction.UPDATE.value
    assert model.entity_type == "product"
    assert model.entity_id == "10"
    assert model.old_values == {"name": "Old name"}
    assert model.new_values == {"name": "New name"}
    assert model.result == AuditResult.SUCCESS.value


def test_model_to_entity():
    created_at = datetime.now(timezone.utc)

    model = AuditLogModel(
        user_id=2,
        action=AuditAction.CREATE.value,
        entity_type="category",
        entity_id="5",
        old_values=None,
        new_values={"name": "Electronics"},
        result=AuditResult.SUCCESS.value,
    )

    model.id = 99
    model.created_at = created_at

    entity = AuditLogMapper.model_to_entity(model)

    assert isinstance(entity, AuditLog)
    assert entity.id == 99
    assert entity.user_id == 2
    assert entity.action == AuditAction.CREATE
    assert entity.entity_type == "category"
    assert entity.entity_id == "5"
    assert entity.old_values is None
    assert entity.new_values == {"name": "Electronics"}
    assert entity.result == AuditResult.SUCCESS
    assert entity.created_at == created_at