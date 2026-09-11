from dataclasses import dataclass
from datetime import datetime

from app.domain.entities.sale_item import SaleItem
from app.domain.entities.sale_status import SaleStatus


@dataclass
class Sale:
    id: int | None
    seller_id: int
    items: list[SaleItem]
    status: SaleStatus = SaleStatus.COMPLETED
    created_at: datetime | None = None

    @property
    def total(self) -> float:
        return sum(item.subtotal for item in self.items)

    def validate(self) -> None:
        if self.seller_id <= 0:
            raise ValueError("Seller ID must be greater than zero")

        if not self.items:
            raise ValueError("Sale must contain at least one item")

        for item in self.items:
            item.validate()