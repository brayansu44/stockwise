from app.domain.entities.product import Product
from app.domain.repositories.product_repository import ProductRepository


class GetProductByCodeUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self, code: str) -> Product:
        product = self.product_repository.get_by_code(code)

        if not product:
            raise ValueError("Product not found")

        return product