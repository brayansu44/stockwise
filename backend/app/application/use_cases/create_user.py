from app.domain.entities.audit_action import AuditAction
from app.domain.entities.audit_log import AuditLog
from app.domain.entities.audit_result import AuditResult
from app.domain.entities.user import User

from app.domain.repositories.audit_log_repository import (
    AuditLogRepository,
)
from app.domain.repositories.password_hasher import PasswordHasher
from app.domain.repositories.user_repository import UserRepository
from app.domain.unit_of_work import UnitOfWork


class CreateUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        audit_log_repository: AuditLogRepository,
        unit_of_work: UnitOfWork,
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.audit_log_repository = audit_log_repository
        self.unit_of_work = unit_of_work

    def execute(
        self,
        user: User,
        plain_password: str,
        created_by_user_id: int,
    ) -> User:
        if created_by_user_id <= 0:
            raise ValueError(
                "Creating user ID must be greater than zero"
            )

        existing_user = self.user_repository.get_by_email(user.email)

        if existing_user:
            raise ValueError("User email already exists")

        if not user.name.strip():
            raise ValueError("User name cannot be empty")

        if not user.email.strip():
            raise ValueError("User email cannot be empty")

        if len(plain_password) < 8:
            raise ValueError(
                "Password must be at least 8 characters long"
            )

        user.hashed_password = self.password_hasher.hash(
            plain_password
        )

        try:
            created_user = self.user_repository.create_without_commit(
                user
            )

            if created_user.id is None:
                raise ValueError("User ID was not generated")

            audit_log = AuditLog(
                id=None,
                user_id=created_by_user_id,
                action=AuditAction.CREATE,
                entity_type="user",
                entity_id=str(created_user.id),
                old_values=None,
                new_values={
                    "name": created_user.name,
                    "role": created_user.role.value,
                    "is_active": created_user.is_active,
                },
                result=AuditResult.SUCCESS,
            )

            audit_log.validate()

            self.audit_log_repository.create_without_commit(
                audit_log
            )

            self.unit_of_work.commit()

            return created_user

        except Exception:
            self.unit_of_work.rollback()
            raise