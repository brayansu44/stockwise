from fastapi import APIRouter, Depends, HTTPException, status

from app.application.dto.product_dto import CreateProductRequest, ProductResponse, UpdateProductRequest
from app.application.use_cases.create_product import CreateProductUseCase
from app.application.use_cases.update_product import UpdateProductUseCase
from app.application.use_cases.change_product_status import (
    ChangeProductStatusUseCase,
)
from app.domain.entities.product import Product
from app.application.use_cases.list_products import ListProductsUseCase
from app.application.use_cases.get_product_by_code import GetProductByCodeUseCase
from app.application.use_cases.list_low_stock_products import (
    ListLowStockProductsUseCase,
)
from app.presentation.dependencies.product_dependencies import (
    get_create_product_use_case,
    get_list_products_use_case,
    get_product_by_code_use_case,
    get_update_product_use_case,
    get_change_product_status_use_case,
    get_list_low_stock_products_use_case,
)
from app.application.mappers.product_mapper import ProductMapper

from app.domain.entities.user import User
from app.presentation.dependencies.auth_dependencies import get_current_user
from app.domain.entities.user_role import UserRole
from app.presentation.dependencies.role_dependencies import require_roles


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    request: CreateProductRequest,
    use_case: CreateProductUseCase = Depends(get_create_product_use_case),
    _current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.INVENTORY_OPERATOR,
        )
    ),
) -> ProductResponse:
    try:
        product = ProductMapper.request_to_entity(request)

        created_product = use_case.execute(product)

        return ProductMapper.entity_to_response(created_product)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    
@router.get(
    "/",
    response_model=list[ProductResponse],
)
def list_products(
    use_case: ListProductsUseCase = Depends(get_list_products_use_case),
    current_user: User = Depends(get_current_user),
) -> list[ProductResponse]:
    products = use_case.execute()

    return [
        ProductMapper.entity_to_response(product)
        for product in products
    ]

@router.get(
    "/low-stock",
    response_model=list[ProductResponse],
)
def list_low_stock_products(
    use_case: ListLowStockProductsUseCase = Depends(
        get_list_low_stock_products_use_case
    ),
    current_user: User = Depends(get_current_user),
) -> list[ProductResponse]:
    products = use_case.execute()

    return [
        ProductMapper.entity_to_response(product)
        for product in products
    ]

@router.get("/{code}", response_model=ProductResponse)
def get_product_by_code(
    code: str,
    use_case: GetProductByCodeUseCase = Depends(get_product_by_code_use_case)
):
    try:
        product = use_case.execute(code)
        return ProductMapper.entity_to_response(product)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
    
@router.patch(
    "/{code}",
    response_model=ProductResponse,
)
def update_product(
    code: str,
    request: UpdateProductRequest,
    use_case: UpdateProductUseCase = Depends(get_update_product_use_case),
    _current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.INVENTORY_OPERATOR,
        )
    ),
) -> ProductResponse:
    try:
        updated_product = use_case.execute(
            code=code,
            name=request.name,
            description=request.description,
            price=request.price,
            minimum_stock=request.minimum_stock,
        )

        return ProductMapper.entity_to_response(updated_product)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
        
@router.patch(
    "/{code}/activate",
    response_model=ProductResponse,
)
def activate_product(
    code: str,
    use_case: ChangeProductStatusUseCase = Depends(
        get_change_product_status_use_case
    ),
    _current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.INVENTORY_OPERATOR,
        )
    ),
) -> ProductResponse:
    try:
        product = use_case.execute(
            code=code,
            is_active=True,
        )

        return ProductMapper.entity_to_response(product)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.patch(
    "/{code}/deactivate",
    response_model=ProductResponse,
)
def deactivate_product(
    code: str,
    use_case: ChangeProductStatusUseCase = Depends(
        get_change_product_status_use_case
    ),
    _current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.INVENTORY_OPERATOR,
        )
    ),
) -> ProductResponse:
    try:
        product = use_case.execute(
            code=code,
            is_active=False,
        )

        return ProductMapper.entity_to_response(product)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc