from app.application.use_cases.create_product import CreateProductUseCase
from app.infrastructure.repositories.in_memory_product_repository import InMemoryProductRepository


product_repository = InMemoryProductRepository()


def get_create_product_use_case() -> CreateProductUseCase:
    return CreateProductUseCase(product_repository)