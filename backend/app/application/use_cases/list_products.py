from app.domain.entities.product import Product
from app.domain.repositories.product_repository import ProductRepository


class ListProductsUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self) -> list[Product]:
        return self.product_repository.list_all()