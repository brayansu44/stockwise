from app.domain.entities.category import Category
from app.domain.repositories.category_repository import CategoryRepository


class ChangeCategoryStatusUseCase:
    def __init__(
        self,
        category_repository: CategoryRepository,
    ):
        self.category_repository = category_repository

    def execute(
        self,
        category_id: int,
        is_active: bool,
    ) -> Category:
        category = self.category_repository.get_by_id(category_id)

        if category is None:
            raise ValueError("Category not found")

        category.is_active = is_active

        return self.category_repository.update(category)