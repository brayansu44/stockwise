import pytest

from app.application.use_cases.change_user_status import ChangeUserStatusUseCase
from app.domain.entities.user import User
from app.domain.entities.user_role import UserRole


class FakeUserRepository:

    def __init__(self, users=None):
        self.users = users or []

    def get_by_id(self, user_id):
        return next(
            (
                user
                for user in self.users
                if user.id == user_id
            ),
            None,
        )

    def update(self, user):
        return user

def test_deactivate_user_successfully():

    user = User(
        id=1,
        name="Seller User",
        email="seller@test.com",
        hashed_password="hashed_password",
        role=UserRole.SELLER,
        is_active=True,
    )

    user_repository = FakeUserRepository(
        users=[user],
    )

    use_case = ChangeUserStatusUseCase(
        user_repository=user_repository,
    )

    result = use_case.execute(
        user_id=1,
        is_active=False,
    )

    assert result.id == 1
    assert result.is_active is False

def test_activate_user_successfully():

    user = User(
        id=1,
        name="Seller User",
        email="seller@test.com",
        hashed_password="hashed_password",
        role=UserRole.SELLER,
        is_active=False,
    )

    user_repository = FakeUserRepository(
        users=[user],
    )

    use_case = ChangeUserStatusUseCase(
        user_repository=user_repository,
    )

    result = use_case.execute(
        user_id=1,
        is_active=True,
    )

    assert result.id == 1
    assert result.is_active is True

def test_change_user_status_not_found():

    user_repository = FakeUserRepository()

    use_case = ChangeUserStatusUseCase(
        user_repository=user_repository,
    )

    with pytest.raises(
        ValueError,
        match="User not found",
    ):
        use_case.execute(
            user_id=999,
            is_active=False,
        )


