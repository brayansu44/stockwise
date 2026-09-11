from dataclasses import dataclass


@dataclass
class SaleItem:
    product_id: int
    quantity: int
    unit_price: float

    @property
    def subtotal(self) -> float:
        return self.quantity * self.unit_price

    def validate(self) -> None:
        if self.product_id <= 0:
            raise ValueError("Product ID must be greater than zero")

        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        if self.unit_price < 0:
            raise ValueError("Unit price cannot be negative")