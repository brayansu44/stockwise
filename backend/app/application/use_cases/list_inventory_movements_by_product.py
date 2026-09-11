from app.domain.entities.inventory_movement import InventoryMovement
from app.domain.repositories.inventory_movement_repository import (
    InventoryMovementRepository,
)
from app.domain.repositories.product_repository import ProductRepository


class ListInventoryMovementsByProductUseCase:
    def __init__(
        self,
        inventory_movement_repository: InventoryMovementRepository,
        product_repository: ProductRepository,
    ):
        self.inventory_movement_repository = inventory_movement_repository
        self.product_repository = product_repository

    def execute(
        self,
        product_code: str,
    ) -> list[InventoryMovement]:
        product = self.product_repository.get_by_code(product_code)

        if not product:
            raise ValueError("Product not found")

        if product.id is None:
            raise ValueError("Product ID is missing")

        return self.inventory_movement_repository.list_by_product(
            product.id
        )