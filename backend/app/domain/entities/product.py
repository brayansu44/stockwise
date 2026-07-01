from dataclasses import dataclass


@dataclass
class Product:
    id: int | None
    name: str
    code: str
    description: str | None
    price: float
    current_stock: int
    minimum_stock: int
    is_active: bool = True

    def is_low_stock(self) -> bool:
        return self.current_stock <= self.minimum_stock

    def increase_stock(self, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        self.current_stock += quantity

    def decrease_stock(self, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        if quantity > self.current_stock:
            raise ValueError("Insufficient stock")

        self.current_stock -= quantity