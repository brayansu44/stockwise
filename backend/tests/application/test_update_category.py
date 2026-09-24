import pytest

from app.application.use_cases.update_category import (
    UpdateCategoryUseCase,
)
from app.domain.entities.category import Category


class FakeCategoryRepository:

    def __init__(self):
        self.categories: list[Category] = []

    def create(self, category: Category) -> Category:
        category.id = len(self.categories) + 1
        self.categories.append(category)
        return category

    def get_by_id(self, category_id: int) -> Category | None:
        for category in self.categories:
            if category.id == category_id:
                return category
        return None

    def get_by_name(self, name: str) -> Category | None:
        for category in self.categories:
            if category.name.lower() == name.lower():
                return category
        return None

    def list_all(self) -> list[Category]:
        return self.categories

    def update(self, category: Category) -> Category:
        return category


def test_update_category_successfully():

    category_repository = FakeCategoryRepository()

    category_repository.create(
        Category(
            id=None,
            name="Electronics",
            description="Electronic products",
            is_active=True,
        )
    )

    use_case = UpdateCategoryUseCase(
        category_repository=category_repository
    )

    result = use_case.execute(
        category_id=1,
        name="  Computers  ",
        description="Computer products",
    )

    assert result.id == 1
    assert result.name == "Computers"
    assert result.description == "Computer products"


def test_update_category_not_found():

    category_repository = FakeCategoryRepository()

    use_case = UpdateCategoryUseCase(
        category_repository=category_repository
    )

    with pytest.raises(
        ValueError,
        match="Category not found",
    ):
        use_case.execute(
            category_id=999,
            name="Computers",
            description="Computer products",
        )


def test_update_category_empty_name():

    category_repository = FakeCategoryRepository()

    category_repository.create(
        Category(
            id=None,
            name="Electronics",
            description="Electronic products",
            is_active=True,
        )
    )

    use_case = UpdateCategoryUseCase(
        category_repository=category_repository
    )

    with pytest.raises(
        ValueError,
        match="Category name cannot be empty",
    ):
        use_case.execute(
            category_id=1,
            name="   ",
            description="Computer products",
        )


def test_update_category_name_already_exists():

    category_repository = FakeCategoryRepository()

    category_repository.create(
        Category(
            id=None,
            name="Electronics",
            description="Electronic products",
            is_active=True,
        )
    )

    category_repository.create(
        Category(
            id=None,
            name="Computers",
            description="Computer products",
            is_active=True,
        )
    )

    use_case = UpdateCategoryUseCase(
        category_repository=category_repository
    )

    with pytest.raises(
        ValueError,
        match="Category name already exists",
    ):
        use_case.execute(
            category_id=1,
            name="Computers",
            description="Updated description",
        )