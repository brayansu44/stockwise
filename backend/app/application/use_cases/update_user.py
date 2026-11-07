from app.domain.entities.audit_action import AuditAction
from app.domain.entities.audit_log import AuditLog
from app.domain.entities.audit_result import AuditResult
from app.domain.entities.user import User

from app.domain.repositories.audit_log_repository import (
    AuditLogRepository,
)
from app.domain.repositories.user_repository import UserRepository
from app.domain.unit_of_work import UnitOfWork


class UpdateUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        audit_log_repository: AuditLogRepository,
        unit_of_work: UnitOfWork,
    ):
        self.user_repository = user_repository
        self.audit_log_repository = audit_log_repository
        self.unit_of_work = unit_of_work

    def execute(
        self,
        user_id: int,
        name: str,
        email: str,
        role,
        updated_by_user_id: int,
    ) -> User:
        if updated_by_user_id <= 0:
            raise ValueError(
                "Updating user ID must be greater than zero"
            )

        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise ValueError("User not found")

        existing_user = self.user_repository.get_by_email(email)

        if existing_user and existing_user.id != user_id:
            raise ValueError("Email already registered")

        # Capture previous values before modifying the entity
        old_values = {
            "name": user.name,
            "role": user.role.value,
        }

        user.name = name
        user.email = email
        user.role = role

        new_values = {
            "name": user.name,
            "role": user.role.value,
        }

        # Audit only fields that actually changed
        changed_fields = {
            field
            for field in old_values
            if old_values[field] != new_values[field]
        }

        audit_old_values = {
            field: old_values[field]
            for field in changed_fields
        }

        audit_new_values = {
            field: new_values[field]
            for field in changed_fields
        }

        try:
            updated_user = self.user_repository.update_without_commit(
                user
            )

            audit_log = AuditLog(
                id=None,
                user_id=updated_by_user_id,
                action=AuditAction.UPDATE,
                entity_type="user",
                entity_id=str(updated_user.id),
                old_values=audit_old_values,
                new_values=audit_new_values,
                result=AuditResult.SUCCESS,
            )

            audit_log.validate()

            self.audit_log_repository.create_without_commit(
                audit_log
            )

            self.unit_of_work.commit()

            return updated_user

        except Exception:
            self.unit_of_work.rollback()
            raise