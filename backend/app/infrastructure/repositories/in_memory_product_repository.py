from app.domain.entities.product import Product
from app.domain.repositories.product_repository import ProductRepository


class InMemoryProductRepository(ProductRepository):
    def __init__(self):
        self.products: list[Product] = []
        self.current_id = 1

    def create(self, product: Product) -> Product:
        product.id = self.current_id
        self.current_id += 1
        self.products.append(product)
        return product

    def get_by_code(self, code: str) -> Product | None:
        for product in self.products:
            if product.code == code:
                return product

        return None
    
    def list_all(self) -> list[Product]:
        return self.products