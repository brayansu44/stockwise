import pytest

from app.application.mappers.user_mapper import UserMapper
from app.domain.entities.user import User
from app.domain.entities.user_role import UserRole


def test_entity_to_response_without_id():
    user = User(
        id=None,
        name="Test User",
        email="test@example.com",
        hashed_password="hashed_password",
        role=UserRole.ADMIN,
    )

    with pytest.raises(
        ValueError,
        match="User ID cannot be None",
    ):
        UserMapper.entity_to_response(user)