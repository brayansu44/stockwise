from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.domain.entities.user import User
from app.infrastructure.repositories.postgres_user_repository import (
    PostgresUserRepository,
)
from app.infrastructure.security.jwt_token_service import JwtTokenService
from app.presentation.dependencies.user_dependencies import (
    get_token_service,
    get_user_repository,
)


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    token_service: JwtTokenService = Depends(get_token_service),
    user_repository: PostgresUserRepository = Depends(get_user_repository),
) -> User:
    try:
        subject = token_service.decode_access_token(
            credentials.credentials
        )

        user_id = int(subject)

        user = user_repository.get_by_id(user_id)

        if not user:
            raise ValueError("User not found")

        if not user.is_active:
            raise ValueError("User is inactive")

        return user

    except (ValueError, TypeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc