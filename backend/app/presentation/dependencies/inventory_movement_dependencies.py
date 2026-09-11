from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.use_cases.create_inventory_movement import (
    CreateInventoryMovementUseCase,
)
from app.infrastructure.repositories.postgres_inventory_movement_repository import (
    PostgresInventoryMovementRepository,
)
from app.application.use_cases.list_inventory_movements_by_product import (
    ListInventoryMovementsByProductUseCase,
)
from app.presentation.dependencies.database_dependencies import (
    get_db_session,
)
from app.presentation.dependencies.product_dependencies import (
    get_product_repository,
)


def get_inventory_movement_repository(
    db_session: Session = Depends(get_db_session),
) -> PostgresInventoryMovementRepository:
    return PostgresInventoryMovementRepository(db_session)


def get_create_inventory_movement_use_case(
    inventory_movement_repository: PostgresInventoryMovementRepository = Depends(
        get_inventory_movement_repository
    ),
    product_repository=Depends(get_product_repository),
) -> CreateInventoryMovementUseCase:
    return CreateInventoryMovementUseCase(
        inventory_movement_repository=inventory_movement_repository,
        product_repository=product_repository,
    )
    
def get_list_inventory_movements_by_product_use_case(
    inventory_movement_repository: PostgresInventoryMovementRepository = Depends(
        get_inventory_movement_repository
    ),
    product_repository=Depends(get_product_repository),
) -> ListInventoryMovementsByProductUseCase:
    return ListInventoryMovementsByProductUseCase(
        inventory_movement_repository=inventory_movement_repository,
        product_repository=product_repository,
    )