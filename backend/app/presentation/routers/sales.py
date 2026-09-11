from fastapi import APIRouter, Depends, HTTPException, status

from app.application.dto.sale_dto import (
    CreateSaleRequest,
    SaleResponse,
)
from app.application.mappers.sale_mapper import SaleMapper
from app.application.use_cases.create_sale import CreateSaleUseCase
from app.domain.entities.user import User
from app.domain.entities.user_role import UserRole
from app.application.use_cases.get_sale_by_id import GetSaleByIdUseCase
from app.application.use_cases.list_sales import ListSalesUseCase
from app.presentation.dependencies.role_dependencies import require_roles
from app.presentation.dependencies.sale_dependencies import (
    get_create_sale_use_case,
    get_list_sales_use_case,
    get_sale_by_id_use_case,
)



router = APIRouter(
    prefix="/sales",
    tags=["Sales"],
)


@router.post(
    "/",
    response_model=SaleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_sale(
    request: CreateSaleRequest,
    use_case: CreateSaleUseCase = Depends(
        get_create_sale_use_case
    ),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SELLER,
        )
    ),
) -> SaleResponse:
    try:
        sale = use_case.execute(
            seller_id=current_user.id,
            items=request.items,
        )

        return SaleMapper.entity_to_response(sale)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

@router.get(
    "/{sale_id}",
    response_model=SaleResponse,
)

@router.get(
    "/",
    response_model=list[SaleResponse],
)
def list_sales(
    use_case: ListSalesUseCase = Depends(get_list_sales_use_case),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SELLER,
        )
    ),
) -> list[SaleResponse]:
    sales = use_case.execute()

    return [
        SaleMapper.entity_to_response(sale)
        for sale in sales
    ]

def get_sale_by_id(
    sale_id: int,
    use_case: GetSaleByIdUseCase = Depends(get_sale_by_id_use_case),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SELLER,
        )
    ),
) -> SaleResponse:
    try:
        sale = use_case.execute(sale_id)

        return SaleMapper.entity_to_response(sale)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc