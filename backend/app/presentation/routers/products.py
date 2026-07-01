from fastapi import APIRouter, HTTPException

from app.application.dto.product_dto import CreateProductRequest, ProductResponse
from app.application.use_cases.create_product import CreateProductUseCase
from app.domain.entities.product import Product
from app.infrastructure.repositories.in_memory_product_repository import InMemoryProductRepository


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

product_repository = InMemoryProductRepository()


@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(request: CreateProductRequest):
    product = Product(
        id=None,
        name=request.name,
        code=request.code,
        description=request.description,
        price=request.price,
        current_stock=request.current_stock,
        minimum_stock=request.minimum_stock
    )

    use_case = CreateProductUseCase(product_repository)

    try:
        return use_case.execute(product)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))