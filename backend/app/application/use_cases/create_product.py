from app.domain.entities.product import Product
from app.domain.repositories.category_repository import CategoryRepository
from app.domain.repositories.product_repository import ProductRepository


class CreateProductUseCase:
    def __init__(
        self,
        product_repository: ProductRepository,
        category_repository: CategoryRepository,
    ):
        self.product_repository = product_repository
        self.category_repository = category_repository

    def execute(self, product: Product) -> Product:
        existing_product = self.product_repository.get_by_code(
            product.code
        )

        if existing_product:
            raise ValueError("Product code already exists")

        if product.price < 0:
            raise ValueError("Product price cannot be negative")

        if product.current_stock < 0:
            raise ValueError("Current stock cannot be negative")

        if product.minimum_stock < 0:
            raise ValueError("Minimum stock cannot be negative")

        category = self.category_repository.get_by_id(product.category_id)

        if category is None:
            raise ValueError("Category not found")

        if not category.is_active:
            raise ValueError("Category is inactive")

        return self.product_repository.create(product)