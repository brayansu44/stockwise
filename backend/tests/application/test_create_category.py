from app.application.use_cases.create_category import CreateCategoryUseCase
from app.domain.entities.category import Category
from app.domain.repositories.category_repository import CategoryRepository
import pytest
from app.application.use_cases.list_categories import ListCategoriesUseCase
from app.application.use_cases.get_category_by_id import GetCategoryByIdUseCase
from app.application.use_cases.update_category import UpdateCategoryUseCase
from app.application.use_cases.change_category_status import (
    ChangeCategoryStatusUseCase,
)

class FakeCategoryRepository(CategoryRepository):
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


def test_create_category():
    repository = FakeCategoryRepository()
    use_case = CreateCategoryUseCase(repository)

    category = Category(
        id=None,
        name="Peripherals",
        description="Computer peripherals",
    )

    result = use_case.execute(category)

    assert result.id == 1
    assert result.name == "Peripherals"
    assert result.description == "Computer peripherals"
    assert result.is_active is True
    assert len(repository.categories) == 1
    
def test_create_category_rejects_duplicate_name():
    existing_category = Category(
        id=1,
        name="Peripherals",
        description="Computer peripherals",
    )

    repository = FakeCategoryRepository()
    repository.categories.append(existing_category)

    use_case = CreateCategoryUseCase(repository)

    new_category = Category(
        id=None,
        name="Peripherals",
        description="Another peripherals category",
    )

    with pytest.raises(
        ValueError,
        match="Category name already exists",
    ):
        use_case.execute(new_category)

    assert len(repository.categories) == 1
    
def test_create_category_rejects_duplicate_name_case_insensitive():
    existing_category = Category(
        id=1,
        name="Peripherals",
        description="Computer peripherals",
    )

    repository = FakeCategoryRepository()
    repository.categories.append(existing_category)

    use_case = CreateCategoryUseCase(repository)

    new_category = Category(
        id=None,
        name="peripherals",
        description="Another peripherals category",
    )

    with pytest.raises(
        ValueError,
        match="Category name already exists",
    ):
        use_case.execute(new_category)

    assert len(repository.categories) == 1    

def test_create_category_rejects_duplicate_name_with_whitespace():
    existing_category = Category(
        id=1,
        name="Peripherals",
        description="Computer peripherals",
    )

    repository = FakeCategoryRepository()
    repository.categories.append(existing_category)

    use_case = CreateCategoryUseCase(repository)

    new_category = Category(
        id=None,
        name="  Peripherals  ",
        description="Another peripherals category",
    )

    with pytest.raises(
        ValueError,
        match="Category name already exists",
    ):
        use_case.execute(new_category)

    assert len(repository.categories) == 1

def test_list_categories():
    repository = FakeCategoryRepository()

    repository.create(
        Category(
            id=None,
            name="Peripherals",
            description="Computer peripherals",
        )
    )

    repository.create(
        Category(
            id=None,
            name="Laptops",
            description="Portable computers",
        )
    )

    use_case = ListCategoriesUseCase(repository)

    categories = use_case.execute()

    assert len(categories) == 2
    assert categories[0].name == "Peripherals"
    assert categories[1].name == "Laptops"

def test_get_category_by_id():
    repository = FakeCategoryRepository()

    created_category = repository.create(
        Category(
            id=None,
            name="Peripherals",
            description="Computer peripherals",
        )
    )

    use_case = GetCategoryByIdUseCase(repository)

    category = use_case.execute(created_category.id)

    assert category.id == 1
    assert category.name == "Peripherals"
    assert category.description == "Computer peripherals"
    assert category.is_active is True


def test_get_category_by_id_not_found():
    repository = FakeCategoryRepository()
    use_case = GetCategoryByIdUseCase(repository)

    try:
        use_case.execute(999)
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Category not found"

def test_update_category():
    repository = FakeCategoryRepository()

    category = repository.create(
        Category(
            id=None,
            name="Peripherals",
            description="Computer peripherals",
        )
    )

    use_case = UpdateCategoryUseCase(repository)

    updated_category = use_case.execute(
        category_id=category.id,
        name="Computer Accessories",
        description="Accessories and peripherals",
    )

    assert updated_category.id == 1
    assert updated_category.name == "Computer Accessories"
    assert updated_category.description == "Accessories and peripherals"


def test_update_category_not_found():
    repository = FakeCategoryRepository()
    use_case = UpdateCategoryUseCase(repository)

    try:
        use_case.execute(
            category_id=999,
            name="Peripherals",
            description="Computer peripherals",
        )
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Category not found"


def test_update_category_rejects_duplicate_name():
    repository = FakeCategoryRepository()

    repository.create(
        Category(
            id=None,
            name="Peripherals",
            description=None,
        )
    )

    laptops = repository.create(
        Category(
            id=None,
            name="Laptops",
            description=None,
        )
    )

    use_case = UpdateCategoryUseCase(repository)

    try:
        use_case.execute(
            category_id=laptops.id,
            name="peripherals",
            description=None,
        )
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Category name already exists"


def test_update_category_allows_same_name():
    repository = FakeCategoryRepository()

    category = repository.create(
        Category(
            id=None,
            name="Peripherals",
            description="Old description",
        )
    )

    use_case = UpdateCategoryUseCase(repository)

    updated_category = use_case.execute(
        category_id=category.id,
        name="Peripherals",
        description="Updated description",
    )

    assert updated_category.id == category.id
    assert updated_category.name == "Peripherals"
    assert updated_category.description == "Updated description"

def test_deactivate_category():
    repository = FakeCategoryRepository()

    category = repository.create(
        Category(
            id=None,
            name="Peripherals",
            description="Computer peripherals",
        )
    )

    use_case = ChangeCategoryStatusUseCase(repository)

    updated_category = use_case.execute(
        category_id=category.id,
        is_active=False,
    )

    assert updated_category.id == category.id
    assert updated_category.is_active is False


def test_activate_category():
    repository = FakeCategoryRepository()

    category = repository.create(
        Category(
            id=None,
            name="Peripherals",
            description="Computer peripherals",
            is_active=False,
        )
    )

    use_case = ChangeCategoryStatusUseCase(repository)

    updated_category = use_case.execute(
        category_id=category.id,
        is_active=True,
    )

    assert updated_category.id == category.id
    assert updated_category.is_active is True

def test_change_category_status_not_found():
    repository = FakeCategoryRepository()
    use_case = ChangeCategoryStatusUseCase(repository)

    try:
        use_case.execute(
            category_id=999,
            is_active=False,
        )
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Category not found"
