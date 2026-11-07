from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.use_cases.create_user import CreateUserUseCase
from app.application.use_cases.get_users import GetUsersUseCase
from app.application.use_cases.update_user import UpdateUserUseCase
from app.application.use_cases.change_user_status import ChangeUserStatusUseCase
from app.infrastructure.repositories.postgres_user_repository import (
    PostgresUserRepository,
)
from app.infrastructure.security.password_hasher import Argon2PasswordHasher
from app.presentation.dependencies.database_dependencies import get_db_session
from app.application.use_cases.login_user import LoginUserUseCase
from app.infrastructure.security.jwt_token_service import JwtTokenService

from app.infrastructure.repositories.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)
from app.infrastructure.unit_of_work import SqlAlchemyUnitOfWork

from app.presentation.dependencies.audit_log_dependencies import (
    get_audit_log_repository,
)
from app.presentation.dependencies.unit_of_work_dependencies import (
    get_unit_of_work,
)


def get_user_repository(
    db_session: Session = Depends(get_db_session),
) -> PostgresUserRepository:
    return PostgresUserRepository(db_session)


def get_password_hasher() -> Argon2PasswordHasher:
    return Argon2PasswordHasher()

def get_create_user_use_case(
    user_repository: PostgresUserRepository = Depends(
        get_user_repository
    ),
    password_hasher: Argon2PasswordHasher = Depends(
        get_password_hasher
    ),
    audit_log_repository: PostgresAuditLogRepository = Depends(
        get_audit_log_repository
    ),
    unit_of_work: SqlAlchemyUnitOfWork = Depends(
        get_unit_of_work
    ),
) -> CreateUserUseCase:
    return CreateUserUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
        audit_log_repository=audit_log_repository,
        unit_of_work=unit_of_work,
    )

def get_users_use_case(
    user_repository: PostgresUserRepository = Depends(get_user_repository),
) -> GetUsersUseCase:
    return GetUsersUseCase(
        user_repository=user_repository,
    )

def get_update_user_use_case(
    user_repository: PostgresUserRepository = Depends(
        get_user_repository
    ),
    audit_log_repository: PostgresAuditLogRepository = Depends(
        get_audit_log_repository
    ),
    unit_of_work: SqlAlchemyUnitOfWork = Depends(
        get_unit_of_work
    ),
) -> UpdateUserUseCase:
    return UpdateUserUseCase(
        user_repository=user_repository,
        audit_log_repository=audit_log_repository,
        unit_of_work=unit_of_work,
    )

def get_change_user_status_use_case(
    user_repository: PostgresUserRepository = Depends(
        get_user_repository
    ),
    audit_log_repository: PostgresAuditLogRepository = Depends(
        get_audit_log_repository
    ),
    unit_of_work: SqlAlchemyUnitOfWork = Depends(
        get_unit_of_work
    ),
) -> ChangeUserStatusUseCase:
    return ChangeUserStatusUseCase(
        user_repository=user_repository,
        audit_log_repository=audit_log_repository,
        unit_of_work=unit_of_work,
    )

def get_token_service() -> JwtTokenService:
    return JwtTokenService()


def get_login_user_use_case(
    user_repository: PostgresUserRepository = Depends(
        get_user_repository
    ),
    password_hasher: Argon2PasswordHasher = Depends(
        get_password_hasher
    ),
    token_service: JwtTokenService = Depends(
        get_token_service
    ),
    audit_log_repository: PostgresAuditLogRepository = Depends(
        get_audit_log_repository
    ),
    unit_of_work: SqlAlchemyUnitOfWork = Depends(
        get_unit_of_work
    ),
) -> LoginUserUseCase:
    return LoginUserUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
        token_service=token_service,
        audit_log_repository=audit_log_repository,
        unit_of_work=unit_of_work,
    )