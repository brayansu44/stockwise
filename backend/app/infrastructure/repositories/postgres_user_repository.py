from sqlalchemy.orm import Session

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.database.models.user_model import UserModel


class PostgresUserRepository(UserRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, user: User) -> User:
        user_model = UserModel(
            name=user.name,
            email=user.email,
            hashed_password=user.hashed_password,
            role=user.role,
            is_active=user.is_active,
        )

        self.db_session.add(user_model)
        self.db_session.commit()
        self.db_session.refresh(user_model)

        return self._to_entity(user_model)

    def get_by_email(self, email: str) -> User | None:
        user_model = (
            self.db_session.query(UserModel)
            .filter(UserModel.email == email)
            .first()
        )

        if not user_model:
            return None

        return self._to_entity(user_model)

    def get_by_id(self, user_id: int) -> User | None:
        user_model = (
            self.db_session.query(UserModel)
            .filter(UserModel.id == user_id)
            .first()
        )

        if not user_model:
            return None

        return self._to_entity(user_model)

    def _to_entity(self, user_model: UserModel) -> User:
        return User(
            id=user_model.id,
            name=user_model.name,
            email=user_model.email,
            hashed_password=user_model.hashed_password,
            role=user_model.role,
            is_active=user_model.is_active,
        )