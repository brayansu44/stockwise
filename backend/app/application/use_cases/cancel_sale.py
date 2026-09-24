
from app.domain.entities.inventory_movement import InventoryMovement
from app.domain.entities.movement_type import MovementType
from app.domain.entities.sale import Sale
from app.domain.entities.sale_status import SaleStatus
from app.domain.entities.product import Product

from app.domain.repositories.inventory_movement_repository import (
    InventoryMovementRepository,
)
from app.domain.repositories.product_repository import ProductRepository
from app.domain.repositories.sale_repository import SaleRepository
from app.domain.unit_of_work import UnitOfWork


class CancelSaleUseCase:

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

    def execute(self, sale_id: int) -> Sale:

        if sale_id <= 0:
            raise ValueError(
                "Sale ID must be greater than zero"
            )

        sale = self.sale_repository.get_by_id(sale_id)

        if not sale:
            raise ValueError("Sale not found")

        if sale.status == SaleStatus.CANCELLED:
            raise ValueError("Sale is already cancelled")

        products_to_restore: list[tuple[Product, int]] = []

        # Validate all products before modifying stock
        for item in sale.items:
            product = self.product_repository.get_by_id(
                item.product_id
            )

            if not product:
                raise ValueError(
                    f"Product not found for sale item: {item.product_id}"
                )

            products_to_restore.append(
                (product, item.quantity)
            )

        # Execute all changes in one transaction
        try:
            # Restore stock and register inventory movements
            for product, quantity in products_to_restore:
                product.increase_stock(quantity)

                self.product_repository.update_without_commit(
                    product
                )

                movement = InventoryMovement(
                    id=None,
                    product_id=product.id,
                    movement_type=MovementType.ENTRY,
                    quantity=quantity,
                    reason=f"Sale cancellation #{sale.id}",
                    sale_id=sale.id,
                )

                movement.validate()

                self.inventory_movement_repository.create_without_commit(
                    movement
                )

            # Update sale status
            sale.status = SaleStatus.CANCELLED

            self.sale_repository.update_without_commit(
                sale
            )

            # Confirm all changes
            self.unit_of_work.commit()

            return sale

        except Exception:
            # Revert pending database changes
            self.unit_of_work.rollback()
            raise