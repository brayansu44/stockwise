from app.application.use_cases.create_product import CreateProductUseCase
from app.infrastructure.repositories.in_memory_product_repository import InMemoryProductRepository
from app.application.use_cases.list_products import ListProductsUseCase
from app.application.use_cases.get_product_by_code import GetProductByCodeUseCase

product_repository = InMemoryProductRepository()


def get_create_product_use_case() -> CreateProductUseCase:
    return CreateProductUseCase(product_repository)

def get_list_products_use_case() -> ListProductsUseCase:
    return ListProductsUseCase(product_repository)

def get_product_by_code_use_case() -> GetProductByCodeUseCase:
    return GetProductByCodeUseCase(product_repository)