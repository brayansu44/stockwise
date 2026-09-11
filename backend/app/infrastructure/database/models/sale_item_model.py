from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.database import Base


class SaleItemModel(Base):
    __tablename__ = "sale_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    sale_id: Mapped[int] = mapped_column(
        ForeignKey("sales.id"),
        index=True,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        index=True,
    )

    quantity: Mapped[int]

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
    )