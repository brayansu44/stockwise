from fastapi import APIRouter, Depends, HTTPException, status

from app.application.dto.product_dto import CreateProductRequest, ProductResponse
from app.application.use_cases.create_product import CreateProductUseCase
from app.domain.entities.product import Product
from app.application.use_cases.list_products import ListProductsUseCase
from app.application.use_cases.get_product_by_code import GetProductByCodeUseCase
from app.presentation.dependencies.product_dependencies import (
    get_create_product_use_case,
    get_list_products_use_case,
    get_product_by_code_use_case
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