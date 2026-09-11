from abc import ABC, abstractmethod

from app.domain.entities.inventory_movement import InventoryMovement


class InventoryMovementRepository(ABC):
    @abstractmethod
    def create(
        self,
        movement: InventoryMovement,
    ) -> InventoryMovement:
        pass
    
    @abstractmethod
    def create_without_commit(
        self,
        movement: InventoryMovement,
    ) -> InventoryMovement:
        pass

    @abstractmethod
    def list_by_product(
        self,
        product_id: int,
    ) -> list[InventoryMovement]:
        pass