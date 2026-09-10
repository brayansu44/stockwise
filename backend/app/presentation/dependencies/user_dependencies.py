from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.use_cases.create_user import CreateUserUseCase
from app.infrastructure.repositories.postgres_user_repository import (
    PostgresUserRepository,
)
from app.infrastructure.security.password_hasher import Argon2PasswordHasher
from app.presentation.dependencies.database_dependencies import get_db_session
from app.application.use_cases.login_user import LoginUserUseCase
from app.infrastructure.security.jwt_token_service import JwtTokenService


def get_user_repository(
    db_session: Session = Depends(get_db_session),
) -> PostgresUserRepository:
    return PostgresUserRepository(db_session)


def get_password_hasher() -> Argon2PasswordHasher:
    return Argon2PasswordHasher()


def get_create_user_use_case(
    user_repository: PostgresUserRepository = Depends(get_user_repository),
    password_hasher: Argon2PasswordHasher = Depends(get_password_hasher),
) -> CreateUserUseCase:
    return CreateUserUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
    )

def get_token_service() -> JwtTokenService:
    return JwtTokenService()


def get_login_user_use_case(
    user_repository: PostgresUserRepository = Depends(get_user_repository),
    password_hasher: Argon2PasswordHasher = Depends(get_password_hasher),
    token_service: JwtTokenService = Depends(get_token_service),
) -> LoginUserUseCase:
    return LoginUserUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
        token_service=token_service,
    )