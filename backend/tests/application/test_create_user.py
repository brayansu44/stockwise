import pytest

from app.application.use_cases.create_user import CreateUserUseCase
from app.domain.entities.user import User
from app.domain.entities.user_role import UserRole


class FakeUserRepository:

    def __init__(self, users=None):
        self.users = users or []

    def get_by_email(self, email):
        return next(
            (
                user
                for user in self.users
                if user.email == email
            ),
            None,
        )

    def create(self, user):
        if user.id is None:
            user.id = len(self.users) + 1

        self.users.append(user)

        return user


class FakePasswordHasher:

    def hash(self, password):
        return f"hashed:{password}"


def test_create_user_successfully():

    user_repository = FakeUserRepository()
    password_hasher = FakePasswordHasher()

    use_case = CreateUserUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
    )

    user = User(
        id=None,
        name="New Seller",
        email="seller@test.com",
        hashed_password="",
        role=UserRole.SELLER,
    )

    result = use_case.execute(
        user=user,
        plain_password="SecurePassword123!",
    )

    assert result.id == 1
    assert result.name == "New Seller"
    assert result.email == "seller@test.com"
    assert result.role == UserRole.SELLER
    assert result.hashed_password == "hashed:SecurePassword123!"

    assert len(user_repository.users) == 1


def test_create_user_email_already_exists():

    existing_user = User(
        id=1,
        name="Existing User",
        email="existing@test.com",
        hashed_password="existing_hash",
        role=UserRole.SELLER,
    )

    user_repository = FakeUserRepository(
        users=[existing_user]
    )

    password_hasher = FakePasswordHasher()

    use_case = CreateUserUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
    )

    user = User(
        id=None,
        name="Another User",
        email="existing@test.com",
        hashed_password="",
        role=UserRole.SELLER,
    )

    with pytest.raises(
        ValueError,
        match="User email already exists",
    ):
        use_case.execute(
            user=user,
            plain_password="SecurePassword123!",
        )


def test_create_user_empty_name():

    user_repository = FakeUserRepository()
    password_hasher = FakePasswordHasher()

    use_case = CreateUserUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
    )

    user = User(
        id=None,
        name="   ",
        email="user@test.com",
        hashed_password="",
        role=UserRole.SELLER,
    )

    with pytest.raises(
        ValueError,
        match="User name cannot be empty",
    ):
        use_case.execute(
            user=user,
            plain_password="SecurePassword123!",
        )


def test_create_user_empty_email():

    user_repository = FakeUserRepository()
    password_hasher = FakePasswordHasher()

    use_case = CreateUserUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
    )

    user = User(
        id=None,
        name="Valid User",
        email="   ",
        hashed_password="",
        role=UserRole.SELLER,
    )

    with pytest.raises(
        ValueError,
        match="User email cannot be empty",
    ):
        use_case.execute(
            user=user,
            plain_password="SecurePassword123!",
        )


def test_create_user_password_too_short():

    user_repository = FakeUserRepository()
    password_hasher = FakePasswordHasher()

    use_case = CreateUserUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
    )

    user = User(
        id=None,
        name="Valid User",
        email="valid@test.com",
        hashed_password="",
        role=UserRole.SELLER,
    )

    with pytest.raises(
        ValueError,
        match="Password must be at least 8 characters long",
    ):
        use_case.execute(
            user=user,
            plain_password="1234567",
        )