from app.domain.entities.product import Product
from app.domain.repositories.product_repository import ProductRepository


class UpdateProductUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(
        self,
        code: str,
        name: str | None = None,
        description: str | None = None,
        price: float | None = None,
        minimum_stock: int | None = None,
    ) -> Product:
        product = self.product_repository.get_by_code(code)

        if not product:
            raise ValueError("Product not found")

        if name is not None:
            if not name.strip():
                raise ValueError("Product name cannot be empty")
            product.name = name

        if description is not None:
            product.description = description

        if price is not None:
            if price < 0:
                raise ValueError("Product price cannot be negative")
            product.price = price

        if minimum_stock is not None:
            if minimum_stock < 0:
                raise ValueError("Minimum stock cannot be negative")
            product.minimum_stock = minimum_stock

        return self.product_repository.update(product)