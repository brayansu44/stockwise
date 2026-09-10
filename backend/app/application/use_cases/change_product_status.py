from app.domain.entities.product import Product
from app.domain.repositories.product_repository import ProductRepository


class ChangeProductStatusUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self, code: str, is_active: bool) -> Product:
        product = self.product_repository.get_by_code(code)

        if not product:
            raise ValueError("Product not found")

        product.is_active = is_active

        return self.product_repository.update(product)