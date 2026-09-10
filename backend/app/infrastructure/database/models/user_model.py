from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100)
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        index=True
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255)
    )

    role: Mapped[str] = mapped_column(
        String(50)
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )