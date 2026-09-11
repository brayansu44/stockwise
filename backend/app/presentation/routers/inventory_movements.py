from fastapi import APIRouter, Depends, HTTPException, status

from app.application.dto.inventory_movement_dto import (
    CreateInventoryMovementRequest,
    InventoryMovementResponse,
)
from app.application.mappers.inventory_movement_mapper import (
    InventoryMovementMapper,
)
from app.application.use_cases.create_inventory_movement import (
    CreateInventoryMovementUseCase,
)
from app.domain.entities.user_role import UserRole
from app.presentation.dependencies.inventory_movement_dependencies import (
    get_create_inventory_movement_use_case,
)
from app.presentation.dependencies.role_dependencies import require_roles
from app.application.use_cases.list_inventory_movements_by_product import (
    ListInventoryMovementsByProductUseCase,
)
from app.presentation.dependencies.inventory_movement_dependencies import (
    get_list_inventory_movements_by_product_use_case,
)

router = APIRouter(
    prefix="/inventory-movements",
    tags=["Inventory Movements"],
)


@router.post(
    "/",
    response_model=InventoryMovementResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_inventory_movement(
    request: CreateInventoryMovementRequest,
    use_case: CreateInventoryMovementUseCase = Depends(
        get_create_inventory_movement_use_case
    ),
    _current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.INVENTORY_OPERATOR,
        )
    ),
) -> InventoryMovementResponse:
    try:
        movement = use_case.execute(
            product_code=request.product_code,
            movement_type=request.movement_type,
            quantity=request.quantity,
            reason=request.reason,
        )

        return InventoryMovementMapper.entity_to_response(movement)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
        
@router.get(
    "/product/{product_code}",
    response_model=list[InventoryMovementResponse],
)
def list_inventory_movements_by_product(
    product_code: str,
    use_case: ListInventoryMovementsByProductUseCase = Depends(
        get_list_inventory_movements_by_product_use_case
    ),
    _current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.INVENTORY_OPERATOR,
            UserRole.SELLER,
        )
    ),
) -> list[InventoryMovementResponse]:
    try:
        movements = use_case.execute(product_code)

        return [
            InventoryMovementMapper.entity_to_response(movement)
            for movement in movements
        ]

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc