from app.application.use_cases.get_users import GetUsersUseCase
from app.domain.entities.user import User
from app.domain.entities.user_role import UserRole


class FakeUserRepository:

    def __init__(self, users=None):
        self.users = users or []

    def get_all(self):
        return self.users


def test_get_users_successfully():

    users = [
        User(
            id=1,
            name="Admin User",
            email="admin@test.com",
            hashed_password="hashed_password",
            role=UserRole.ADMIN,
        ),
        User(
            id=2,
            name="Seller User",
            email="seller@test.com",
            hashed_password="hashed_password",
            role=UserRole.SELLER,
        ),
    ]

    user_repository = FakeUserRepository(users=users)

    use_case = GetUsersUseCase(
        user_repository=user_repository,
    )

    result = use_case.execute()

    assert len(result) == 2
    assert result[0].id == 1
    assert result[0].email == "admin@test.com"
    assert result[1].id == 2
    assert result[1].email == "seller@test.com"