from abc import ABC, abstractmethod
from app.domain.entities.product import Product


class ProductRepository(ABC):

    @abstractmethod
    def create(self, product: Product) -> Product:
        pass

    @abstractmethod
    def get_by_code(self, code: str) -> Product | None:
        pass

    @abstractmethod
    def list_all(self) -> list[Product]:
        pass
    
    @abstractmethod
    def update(self, product: Product) -> Product:
        pass
    
    @abstractmethod
    def update_without_commit(
        self,
        product: Product,
    ) -> Product:
        pass