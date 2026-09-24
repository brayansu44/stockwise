from app.application.dto.sale_dto import CreateSaleItemRequest

from app.domain.entities.sale import Sale
from app.domain.entities.sale_item import SaleItem
from app.domain.entities.product import Product
from app.domain.entities.inventory_movement import InventoryMovement
from app.domain.entities.movement_type import MovementType

from app.domain.repositories.product_repository import ProductRepository
from app.domain.repositories.sale_repository import SaleRepository
from app.domain.repositories.inventory_movement_repository import (
    InventoryMovementRepository,
)

from app.domain.unit_of_work import UnitOfWork


class CreateSaleUseCase:

    def __init__(
        self,
        sale_repository: SaleRepository,
        product_repository: ProductRepository,
        inventory_movement_repository: InventoryMovementRepository,
        unit_of_work: UnitOfWork,
    ):
        self.sale_repository = sale_repository
        self.product_repository = product_repository
        self.inventory_movement_repository = inventory_movement_repository
        self.unit_of_work = unit_of_work

    def execute(
        self,
        seller_id: int,
        items: list[CreateSaleItemRequest],
    ) -> Sale:

        # Validate seller
        if seller_id <= 0:
            raise ValueError(
                "Seller ID must be greater than zero"
            )

        # Validate sale items
        if not items:
            raise ValueError(
                "Sale must contain at least one item"
            )

        sale_items: list[SaleItem] = []
        products_to_update: list[tuple[Product, int]] = []
        product_codes: set[str] = set()

        # Check duplicate products
        for item in items:
            product_code = item.product_code.strip()

            if product_code in product_codes:
                raise ValueError(
                    f"Duplicate product in sale: {product_code}"
                )

            product_codes.add(product_code)

        # Validate products and available stock
        for item in items:
            product_code = item.product_code.strip()

            product = self.product_repository.get_by_code(
                product_code
            )

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

            if item.quantity > product.current_stock:
                raise ValueError(
                    "Insufficient stock"
                )

            sale_item = SaleItem(
                product_id=product.id,
                quantity=item.quantity,
                unit_price=product.price,
            )

            sale_item.validate()

            sale_items.append(sale_item)

            products_to_update.append(
                (product, item.quantity)
            )

        # Create sale entity
        sale = Sale(
            id=None,
            seller_id=seller_id,
            items=sale_items,
        )

        sale.validate()

        # Execute all database operations in one transaction
        try:

            # Update product stock
            for product, quantity in products_to_update:
                product.decrease_stock(quantity)

                self.product_repository.update_without_commit(
                    product
                )

            # Create sale and sale items
            sale = self.sale_repository.create_without_commit(
                sale
            )

            if sale.id is None:
                raise ValueError(
                    "Sale ID was not generated"
                )

            # Register inventory movements
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

            # Confirm all database operations
            self.unit_of_work.commit()

            return sale

        except Exception:

            # Revert all pending database changes
            self.unit_of_work.rollback()

            raise