from app.domain.entities.inventory_movement import InventoryMovement
from app.domain.entities.movement_type import MovementType
from app.domain.repositories.inventory_movement_repository import (
    InventoryMovementRepository,
)
from app.domain.repositories.product_repository import ProductRepository
from app.domain.unit_of_work import UnitOfWork

class CreateInventoryMovementUseCase:
    def __init__(
        self,
        inventory_movement_repository: InventoryMovementRepository,
        product_repository: ProductRepository,
        unit_of_work: UnitOfWork,
    ):
        self.inventory_movement_repository = inventory_movement_repository
        self.product_repository = product_repository
        self.unit_of_work = unit_of_work

    def execute(
        self,
        product_code: str,
        movement_type: MovementType,
        quantity: int,
        reason: str | None = None,
    ) -> InventoryMovement:
        product = self.product_repository.get_by_code(product_code)

        if not product:
            raise ValueError("Product not found")

        if not product.is_active:
            raise ValueError("Product is inactive")

        if movement_type == MovementType.ENTRY:
            product.increase_stock(quantity)

        elif movement_type == MovementType.EXIT:
            product.decrease_stock(quantity)

        elif movement_type == MovementType.ADJUSTMENT:
            if quantity < 0:
                raise ValueError("Adjusted stock cannot be negative")

            product.current_stock = quantity

        try:
            updated_product = self.product_repository.update_without_commit(product)

            movement = InventoryMovement(
                id=None,
                product_id=updated_product.id,
                movement_type=movement_type,
                quantity=quantity,
                reason=reason,
            )

            movement.validate()

            created_movement = (
                self.inventory_movement_repository.create_without_commit(
                    movement
                )
            )

            self.unit_of_work.commit()

            return created_movement

        except Exception:
            self.unit_of_work.rollback()
            raise