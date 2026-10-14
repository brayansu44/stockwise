from dataclasses import dataclass
from datetime import datetime
from typing import Any

from app.domain.entities.audit_action import AuditAction
from app.domain.entities.audit_result import AuditResult


@dataclass
class AuditLog:
    id: int | None
    user_id: int | None
    action: AuditAction
    entity_type: str
    entity_id: str | None
    old_values: dict[str, Any] | None
    new_values: dict[str, Any] | None
    result: AuditResult
    created_at: datetime | None = None

    def validate(self) -> None:
        if not self.entity_type or not self.entity_type.strip():
            raise ValueError("Entity type is required")

        if len(self.entity_type) > 100:
            raise ValueError("Entity type must not exceed 100 characters")

        if self.entity_id is not None and len(self.entity_id) > 100:
            raise ValueError("Entity ID must not exceed 100 characters")

        if self.user_id is not None and self.user_id <= 0:
            raise ValueError("User ID must be greater than zero")