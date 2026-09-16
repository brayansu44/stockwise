from app.domain.repositories.product_repository import ProductRepository


class ListLowStockProductsUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
        
    def execute(self):
        products = self.product_repository.list_all()

        return [
            product
            for product in products
            if product.is_active and product.is_low_stock()
        ]