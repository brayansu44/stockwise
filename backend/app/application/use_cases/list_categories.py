from app.domain.entities.category import Category
from app.domain.repositories.category_repository import CategoryRepository


class ListCategoriesUseCase:
    def __init__(
        self,
        category_repository: CategoryRepository,
    ):
        self.category_repository = category_repository

    def execute(self) -> list[Category]:
        return self.category_repository.list_all()