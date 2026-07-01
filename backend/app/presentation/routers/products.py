from fastapi import APIRouter, Depends, HTTPException

from app.application.dto.product_dto import CreateProductRequest, ProductResponse
from app.application.use_cases.create_product import CreateProductUseCase
from app.domain.entities.product import Product
from app.application.use_cases.list_products import ListProductsUseCase
from app.presentation.dependencies.product_dependencies import (
    get_create_product_use_case,
    get_list_products_use_case,
)


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(
    request: CreateProductRequest,
    use_case: CreateProductUseCase = Depends(get_create_product_use_case)
):
    product = Product(
        id=None,
        name=request.name,
        code=request.code,
        description=request.description,
        price=request.price,
        current_stock=request.current_stock,
        minimum_stock=request.minimum_stock
    )

    try:
        return use_case.execute(product)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    
@router.get("/", response_model=list[ProductResponse])
def list_products(
    use_case: ListProductsUseCase = Depends(get_list_products_use_case)
):
    return use_case.execute()