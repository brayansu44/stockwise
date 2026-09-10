from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.core.config import settings
from app.domain.repositories.token_service import TokenService


class JwtTokenService(TokenService):
    def create_access_token(self, subject: str) -> str:
        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        payload = {
            "sub": subject,
            "exp": expires_at,
        }

        return jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

    def decode_access_token(self, token: str) -> str:
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )

            subject = payload.get("sub")

            if not subject:
                raise ValueError("Invalid token")

            return subject

        except JWTError as exc:
            raise ValueError("Invalid or expired token") from exc