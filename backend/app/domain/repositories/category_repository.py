from abc import ABC, abstractmethod

from app.domain.entities.category import Category


class CategoryRepository(ABC):
    @abstractmethod
    def create(self, category: Category) -> Category:
        pass

    @abstractmethod
    def get_by_id(self, category_id: int) -> Category | None:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Category | None:
        pass

    @abstractmethod
    def list_all(self) -> list[Category]:
        pass

    @abstractmethod
    def update(self, category: Category) -> Category:
        pass