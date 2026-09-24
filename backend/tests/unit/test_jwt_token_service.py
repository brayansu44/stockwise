import pytest
from jose import jwt

from app.core.config import settings
from app.infrastructure.security.jwt_token_service import JwtTokenService


def test_decode_token_without_subject():
    token_service = JwtTokenService()

    token = jwt.encode(
        {"custom": "test"},
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    with pytest.raises(ValueError, match="Invalid token"):
        token_service.decode_access_token(token)