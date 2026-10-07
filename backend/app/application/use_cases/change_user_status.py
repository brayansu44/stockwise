from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository


class ChangeUserStatusUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(
        self,
        user_id: int,
        is_active: bool,
    ) -> User:
        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise ValueError("User not found")

        user.is_active = is_active

        return self.user_repository.update(user)