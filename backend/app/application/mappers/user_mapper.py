from app.application.dto.user_dto import CreateUserRequest, UserResponse
from app.domain.entities.user import User


class UserMapper:

    @staticmethod
    def request_to_entity(request: CreateUserRequest) -> User:
        return User(
            id=None,
            name=request.name,
            email=request.email,
            hashed_password="",
            role=request.role,
        )

    @staticmethod
    def entity_to_response(user: User) -> UserResponse:
        if user.id is None:
            raise ValueError("User ID cannot be None")

        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            is_active=user.is_active,
        )