from app.domain.entities.audit_action import AuditAction
from app.domain.entities.audit_log import AuditLog
from app.domain.entities.audit_result import AuditResult
from app.domain.entities.inventory_movement import InventoryMovement
from app.domain.entities.movement_type import MovementType

from app.domain.repositories.audit_log_repository import (
    AuditLogRepository,
)
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
        audit_log_repository: AuditLogRepository,
        unit_of_work: UnitOfWork,
    ):
        self.inventory_movement_repository = (
            inventory_movement_repository
        )
        self.product_repository = product_repository
        self.audit_log_repository = audit_log_repository
        self.unit_of_work = unit_of_work

    def execute(
        self,
        user_id: int,
        product_code: str,
        movement_type: MovementType,
        quantity: int,
        reason: str | None = None,
    ) -> InventoryMovement:
        if user_id <= 0:
            raise ValueError("User ID must be greater than zero")

        product = self.product_repository.get_by_code(
            product_code
        )

        if not product:
            raise ValueError("Product not found")

        if not product.is_active:
            raise ValueError("Product is inactive")

        previous_stock = product.current_stock

        if movement_type == MovementType.ENTRY:
            product.increase_stock(quantity)

        elif movement_type == MovementType.EXIT:
            product.decrease_stock(quantity)

        elif movement_type == MovementType.ADJUSTMENT:
            if quantity < 0:
                raise ValueError(
                    "Adjusted stock cannot be negative"
                )

            product.current_stock = quantity

        try:
            updated_product = (
                self.product_repository.update_without_commit(
                    product
                )
            )

            movement = InventoryMovement(
                id=None,
                product_id=updated_product.id,
                movement_type=movement_type,
                quantity=quantity,
                reason=reason,
            )

            movement.validate()

            created_movement = (
                self.inventory_movement_repository
                .create_without_commit(
                    movement
                )
            )

            if created_movement.id is None:
                raise ValueError(
                    "Inventory movement ID was not generated"
                )

            action_by_movement_type = {
                MovementType.ENTRY: AuditAction.INVENTORY_ENTRY,
                MovementType.EXIT: AuditAction.INVENTORY_EXIT,
                MovementType.ADJUSTMENT: (
                    AuditAction.INVENTORY_ADJUSTMENT
                ),
            }

            audit_log = AuditLog(
                id=None,
                user_id=user_id,
                action=action_by_movement_type[
                    movement_type
                ],
                entity_type="inventory_movement",
                entity_id=str(created_movement.id),
                old_values={
                    "current_stock": previous_stock,
                },
                new_values={
                    "current_stock": (
                        updated_product.current_stock
                    ),
                    "product_code": product_code,
                    "movement_type": movement_type.value,
                    "quantity": quantity,
                    "reason": reason,
                },
                result=AuditResult.SUCCESS,
            )

            audit_log.validate()

            self.audit_log_repository.create_without_commit(
                audit_log
            )

            self.unit_of_work.commit()

            return created_movement

        except Exception:
            self.unit_of_work.rollback()
            raise