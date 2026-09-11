from app.application.dto.inventory_movement_dto import (
    InventoryMovementResponse,
)
from app.domain.entities.inventory_movement import InventoryMovement


class InventoryMovementMapper:
    @staticmethod
    def entity_to_response(
        movement: InventoryMovement,
    ) -> InventoryMovementResponse:
        return InventoryMovementResponse(
            id=movement.id,
            product_id=movement.product_id,
            movement_type=movement.movement_type,
            quantity=movement.quantity,
            reason=movement.reason,
            sale_id=movement.sale_id,
            created_at=movement.created_at,
        )