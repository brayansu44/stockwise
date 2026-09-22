from app.domain.entities.category import Category
from app.domain.repositories.category_repository import CategoryRepository


class UpdateCategoryUseCase:
    def __init__(
        self,
        category_repository: CategoryRepository,
    ):
        self.category_repository = category_repository

    def execute(
        self,
        category_id: int,
        name: str,
        description: str | None,
    ) -> Category:
        category = self.category_repository.get_by_id(category_id)

        if category is None:
            raise ValueError("Category not found")

        normalized_name = name.strip()

        if not normalized_name:
            raise ValueError("Category name cannot be empty")

        existing_category = self.category_repository.get_by_name(
            normalized_name
        )

        if (
            existing_category is not None
            and existing_category.id != category_id
        ):
            raise ValueError("Category name already exists")

        category.name = normalized_name
        category.description = description

        return self.category_repository.update(category)