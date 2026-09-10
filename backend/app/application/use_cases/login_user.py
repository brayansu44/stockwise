from app.domain.repositories.password_hasher import PasswordHasher
from app.domain.repositories.token_service import TokenService
from app.domain.repositories.user_repository import UserRepository


class LoginUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        token_service: TokenService,
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.token_service = token_service

    def execute(self, email: str, password: str) -> str:
        user = self.user_repository.get_by_email(email)

        if not user:
            raise ValueError("Invalid email or password")

        if not user.is_active:
            raise ValueError("User is inactive")

        is_valid_password = self.password_hasher.verify(
            password,
            user.hashed_password,
        )

        if not is_valid_password:
            raise ValueError("Invalid email or password")

        return self.token_service.create_access_token(
            subject=str(user.id)
        )