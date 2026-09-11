from app.application.dto.sale_dto import CreateSaleItemRequest
from app.domain.entities.sale import Sale
from app.domain.entities.sale_item import SaleItem
from app.domain.repositories.product_repository import ProductRepository
from app.domain.repositories.sale_repository import SaleRepository
from app.domain.entities.inventory_movement import InventoryMovement
from app.domain.entities.movement_type import MovementType
from app.domain.repositories.inventory_movement_repository import (
    InventoryMovementRepository,
)


class CreateSaleUseCase:
    def __init__(
        self,
        sale_repository: SaleRepository,
        product_repository: ProductRepository,
        inventory_movement_repository: InventoryMovementRepository,
    ):
        self.sale_repository = sale_repository
        self.product_repository = product_repository
        self.inventory_movement_repository = inventory_movement_repository

    def execute(
        self,
        seller_id: int,
        items: list[CreateSaleItemRequest],
    ) -> Sale:
        if seller_id <= 0:
            raise ValueError("Seller ID must be greater than zero")

        if not items:
            raise ValueError("Sale must contain at least one item")

        sale_items: list[SaleItem] = []
        products_to_update = []
        product_codes: set[str] = set()

        for item in items:
            product_code = item.product_code.strip()

            if product_code in product_codes:
                raise ValueError(
                    f"Duplicate product in sale: {product_code}"
                )

            product_codes.add(product_code)

            product = self.product_repository.get_by_code(product_code)

            if not product:
                raise ValueError(
                    f"Product not found: {product_code}"
                )

            if not product.is_active:
                raise ValueError(
                    f"Product is inactive: {product_code}"
                )

            if product.id is None:
                raise ValueError(
                    f"Product ID is missing: {product_code}"
                )

            product.decrease_stock(item.quantity)

            sale_item = SaleItem(
                product_id=product.id,
                quantity=item.quantity,
                unit_price=product.price,
            )

            sale_item.validate()

            sale_items.append(sale_item)
            products_to_update.append(product)

        sale = Sale(
            id=None,
            seller_id=seller_id,
            items=sale_items,
        )
        sale.validate()

        for product in products_to_update:
            self.product_repository.update_without_commit(product)

        sale = self.sale_repository.create_without_commit(sale)

        if sale.id is None:
            raise ValueError("Sale ID was not generated")

        for item in sale.items:
            movement = InventoryMovement(
                id=None,
                product_id=item.product_id,
                movement_type=MovementType.EXIT,
                quantity=item.quantity,
                reason=f"Sale #{sale.id}",
                sale_id=sale.id,
            )

            movement.validate()

            self.inventory_movement_repository.create_without_commit(
                movement
            )

        self.sale_repository.commit()

        return sale