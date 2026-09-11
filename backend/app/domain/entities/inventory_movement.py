from dataclasses import dataclass
from datetime import datetime

from app.domain.entities.movement_type import MovementType


@dataclass
class InventoryMovement:
    id: int | None
    product_id: int
    movement_type: MovementType
    quantity: int
    reason: str | None
    sale_id: int | None = None
    created_at: datetime | None = None

    def validate(self) -> None:
        if self.product_id <= 0:
            raise ValueError("Product ID must be greater than zero")

        if self.movement_type in (
            MovementType.ENTRY,
            MovementType.EXIT,
        ):
            if self.quantity <= 0:
                raise ValueError("Quantity must be greater than zero")

        elif self.movement_type == MovementType.ADJUSTMENT:
            if self.quantity < 0:
                raise ValueError("Adjusted stock cannot be negative")

        if self.sale_id is not None and self.sale_id <= 0:
            raise ValueError("Sale ID must be greater than zero")