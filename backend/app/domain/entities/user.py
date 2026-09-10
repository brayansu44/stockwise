from dataclasses import dataclass

from app.domain.entities.user_role import UserRole


@dataclass
class User:
    id: int | None
    name: str
    email: str
    hashed_password: str
    role: UserRole
    is_active: bool = True