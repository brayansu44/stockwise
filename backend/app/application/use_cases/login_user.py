from app.domain.entities.audit_action import AuditAction
from app.domain.entities.audit_log import AuditLog
from app.domain.entities.audit_result import AuditResult

from app.domain.repositories.audit_log_repository import (
    AuditLogRepository,
)
from app.domain.repositories.password_hasher import PasswordHasher
from app.domain.repositories.token_service import TokenService
from app.domain.repositories.user_repository import UserRepository
from app.domain.unit_of_work import UnitOfWork


class AuthenticationRejectedError(ValueError):
    """Raised when user authentication is rejected."""

class LoginUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        token_service: TokenService,
        audit_log_repository: AuditLogRepository,
        unit_of_work: UnitOfWork,
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.token_service = token_service
        self.audit_log_repository = audit_log_repository
        self.unit_of_work = unit_of_work

    def _record_failed_login(
        self,
        user_id: int | None,
    ) -> None:
        audit_log = AuditLog(
            id=None,
            user_id=user_id,
            action=AuditAction.LOGIN_FAILURE,
            entity_type="authentication",
            entity_id=(
                str(user_id)
                if user_id is not None
                else None
            ),
            old_values=None,
            new_values=None,
            result=AuditResult.FAILURE,
        )

        try:
            audit_log.validate()

            self.audit_log_repository.create_without_commit(
                audit_log
            )

            self.unit_of_work.commit()

        except Exception:
            self.unit_of_work.rollback()
            raise

    def execute(self, email: str, password: str) -> str:
        user = self.user_repository.get_by_email(email)

        if not user:
            self._record_failed_login(
                user_id=None,
            )

            raise AuthenticationRejectedError(
                "Invalid email or password"
            )

        if not user.is_active:
            self._record_failed_login(
                user_id=user.id,
            )

            raise AuthenticationRejectedError(
                "Invalid email or password"
            )

        is_valid_password = self.password_hasher.verify(
            password,
            user.hashed_password,
        )

        if not is_valid_password:
            self._record_failed_login(
                user_id=user.id,
            )

            raise AuthenticationRejectedError(
                "Invalid email or password"
            )

        # Generate access token
        access_token = self.token_service.create_access_token(
            subject=str(user.id)
        )

        # Register successful authentication
        audit_log = AuditLog(
            id=None,
            user_id=user.id,
            action=AuditAction.LOGIN_SUCCESS,
            entity_type="authentication",
            entity_id=str(user.id),
            old_values=None,
            new_values=None,
            result=AuditResult.SUCCESS,
        )

        try:
            audit_log.validate()

            self.audit_log_repository.create_without_commit(
                audit_log
            )

            self.unit_of_work.commit()

        except Exception:
            self.unit_of_work.rollback()
            raise

        return access_token