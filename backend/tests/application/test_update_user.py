import pytest

from app.application.use_cases.update_user import UpdateUserUseCase
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

    def get_by_email(self, email):
        return next(
            (
                user
                for user in self.users
                if user.email == email
            ),
            None,
        )

    def update(self, user):
        return user


def test_update_user_successfully():

    existing_user = User(
        id=1,
        name="Old Name",
        email="old@test.com",
        hashed_password="hashed_password",
        role=UserRole.SELLER,
    )

    user_repository = FakeUserRepository(
        users=[existing_user],
    )

    use_case = UpdateUserUseCase(
        user_repository=user_repository,
    )

    result = use_case.execute(
        user_id=1,
        name="Updated Name",
        email="updated@test.com",
        role=UserRole.INVENTORY_OPERATOR,
    )

    assert result.id == 1
    assert result.name == "Updated Name"
    assert result.email == "updated@test.com"
    assert result.role == UserRole.INVENTORY_OPERATOR
    assert result.hashed_password == "hashed_password"
    assert result.is_active is True

def test_update_user_not_found():

    user_repository = FakeUserRepository()

    use_case = UpdateUserUseCase(
        user_repository=user_repository,
    )

    with pytest.raises(
        ValueError,
        match="User not found",
    ):
        use_case.execute(
            user_id=999,
            name="Updated Name",
            email="updated@test.com",
            role=UserRole.SELLER,
        )

def test_update_user_email_already_exists():

    first_user = User(
        id=1,
        name="First User",
        email="first@test.com",
        hashed_password="hashed_password",
        role=UserRole.SELLER,
    )

    second_user = User(
        id=2,
        name="Second User",
        email="second@test.com",
        hashed_password="hashed_password",
        role=UserRole.INVENTORY_OPERATOR,
    )

    user_repository = FakeUserRepository(
        users=[first_user, second_user],
    )

    use_case = UpdateUserUseCase(
        user_repository=user_repository,
    )

    with pytest.raises(
        ValueError,
        match="Email already registered",
    ):
        use_case.execute(
            user_id=2,
            name="Second User",
            email="first@test.com",
            role=UserRole.INVENTORY_OPERATOR,
        )


