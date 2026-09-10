from fastapi import APIRouter, Depends, HTTPException

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


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(
    request: CreateProductRequest,
    use_case: CreateProductUseCase = Depends(get_create_product_use_case)
):
    product = product = ProductMapper.request_to_entity(request)

    try:
        created_product = use_case.execute(product)
        return ProductMapper.entity_to_response(created_product)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    
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