from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository


class GetUsersUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self) -> list[User]:
        return self.user_repository.get_all()