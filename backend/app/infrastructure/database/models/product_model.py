from decimal import Decimal

from sqlalchemy import Boolean, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.database import Base

class ProductModel(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100))

    code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2)
    )

    current_stock: Mapped[int]

    minimum_stock: Mapped[int]

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )