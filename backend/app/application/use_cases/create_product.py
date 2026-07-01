from app.domain.entities.product import Product
from app.domain.repositories.product_repository import ProductRepository


class CreateProductUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self, product: Product) -> Product:
        existing_product = self.product_repository.get_by_code(product.code)

        if existing_product:
            raise ValueError("Product code already exists")

        if product.price < 0:
            raise ValueError("Product price cannot be negative")

        if product.current_stock < 0:
            raise ValueError("Current stock cannot be negative")

        if product.minimum_stock < 0:
            raise ValueError("Minimum stock cannot be negative")

        return self.product_repository.create(product)