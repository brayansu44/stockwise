from app.domain.entities.user import User
from app.domain.repositories.password_hasher import PasswordHasher
from app.domain.repositories.user_repository import UserRepository


class CreateUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    def execute(self, user: User, plain_password: str) -> User:
        existing_user = self.user_repository.get_by_email(user.email)

        if existing_user:
            raise ValueError("User email already exists")

        if not user.name.strip():
            raise ValueError("User name cannot be empty")

        if not user.email.strip():
            raise ValueError("User email cannot be empty")

        if len(plain_password) < 8:
            raise ValueError("Password must be at least 8 characters long")

        user.hashed_password = self.password_hasher.hash(plain_password)

        return self.user_repository.create(user)