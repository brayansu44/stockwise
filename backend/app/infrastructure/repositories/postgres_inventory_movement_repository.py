from sqlalchemy.orm import Session

from app.domain.entities.inventory_movement import InventoryMovement
from app.domain.entities.movement_type import MovementType
from app.domain.repositories.inventory_movement_repository import (
    InventoryMovementRepository,
)
from app.infrastructure.database.models.inventory_movement_model import (
    InventoryMovementModel,
)
from sqlalchemy.exc import SQLAlchemyError


class PostgresInventoryMovementRepository(InventoryMovementRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(
        self,
        movement: InventoryMovement,
    ) -> InventoryMovement:
        try:
            movement_model = InventoryMovementModel(
                product_id=movement.product_id,
                movement_type=movement.movement_type.value,
                quantity=movement.quantity,
                reason=movement.reason,
            )

            self.db_session.add(movement_model)
            self.db_session.commit()
            self.db_session.refresh(movement_model)

            return self._to_entity(movement_model)

        except SQLAlchemyError:
            self.db_session.rollback()
            raise

    def list_by_product(
        self,
        product_id: int,
    ) -> list[InventoryMovement]:
        movement_models = (
            self.db_session.query(InventoryMovementModel)
            .filter(InventoryMovementModel.product_id == product_id)
            .order_by(InventoryMovementModel.created_at.desc())
            .all()
        )

        return [
            self._to_entity(movement_model)
            for movement_model in movement_models
        ]

    @staticmethod
    def _to_entity(
        movement_model: InventoryMovementModel,
    ) -> InventoryMovement:
        return InventoryMovement(
            id=movement_model.id,
            product_id=movement_model.product_id,
            movement_type=MovementType(movement_model.movement_type),
            quantity=movement_model.quantity,
            reason=movement_model.reason,
            created_at=movement_model.created_at,
        )