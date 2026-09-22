from app.domain.entities.category import Category
from app.domain.repositories.category_repository import CategoryRepository


class CreateCategoryUseCase:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def execute(self, category: Category) -> Category:
        existing_category = self.category_repository.get_by_name(
            category.name.lower()
        )

        if existing_category:
            raise ValueError("Category name already exists")

        return self.category_repository.create(category)