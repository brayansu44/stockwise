from app.domain.entities.audit_action import AuditAction
from app.domain.entities.audit_log import AuditLog
from app.domain.entities.audit_result import AuditResult
from app.domain.entities.user import User

from app.domain.repositories.audit_log_repository import (
    AuditLogRepository,
)
from app.domain.repositories.user_repository import UserRepository
from app.domain.unit_of_work import UnitOfWork


class ChangeUserStatusUseCase:
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
        is_active: bool,
        changed_by_user_id: int,
    ) -> User:
        if changed_by_user_id <= 0:
            raise ValueError(
                "Changing user ID must be greater than zero"
            )

        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise ValueError("User not found")

        # Do not record an event if the status is unchanged
        if user.is_active == is_active:
            raise ValueError("User already has the requested status")

        # Capture the previous state before modification
        previous_status = user.is_active

        user.is_active = is_active

        audit_action = (
            AuditAction.ACTIVATE
            if is_active
            else AuditAction.DEACTIVATE
        )

        try:
            updated_user = self.user_repository.update_without_commit(
                user
            )

            audit_log = AuditLog(
                id=None,
                user_id=changed_by_user_id,
                action=audit_action,
                entity_type="user",
                entity_id=str(updated_user.id),
                old_values={
                    "is_active": previous_status,
                },
                new_values={
                    "is_active": updated_user.is_active,
                },
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