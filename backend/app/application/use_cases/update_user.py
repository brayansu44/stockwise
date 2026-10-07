from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository


class UpdateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(
        self,
        user_id: int,
        name: str,
        email: str,
        role,
    ) -> User:
        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise ValueError("User not found")

        existing_user = self.user_repository.get_by_email(email)

        if existing_user and existing_user.id != user_id:
            raise ValueError("Email already registered")

        user.name = name
        user.email = email
        user.role = role

        return self.user_repository.update(user)