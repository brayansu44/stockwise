import pytest

from app.application.use_cases.update_product import UpdateProductUseCase
from app.domain.entities.category import Category
from app.domain.entities.product import Product
from app.domain.repositories.category_repository import CategoryRepository
from app.domain.repositories.product_repository import ProductRepository


class FakeProductRepository(ProductRepository):
    def __init__(self):
        self.products: list[Product] = []

    def create(self, product: Product) -> Product:
        product.id = len(self.products) + 1
        self.products.append(product)
        return product

    def get_by_code(self, code: str) -> Product | None:
        for product in self.products:
            if product.code == code:
                return product

        return None

    def get_by_id(self, product_id: int) -> Product | None:
        for product in self.products:
            if product.id == product_id:
                return product

        return None

    def list_all(self) -> list[Product]:
        return self.products

    def update(self, product: Product) -> Product:
        return product

    def update_without_commit(self, product: Product) -> Product:
        return product


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
    
@pytest.fixture
def product_repository() -> FakeProductRepository:
    return FakeProductRepository()


@pytest.fixture
def category_repository() -> FakeCategoryRepository:
    return FakeCategoryRepository()


@pytest.fixture
def use_case(
    product_repository: FakeProductRepository,
    category_repository: FakeCategoryRepository,
) -> UpdateProductUseCase:
    return UpdateProductUseCase(
        product_repository,
        category_repository,
    )
    
def test_update_product_without_changing_category(
    product_repository: FakeProductRepository,
    use_case: UpdateProductUseCase,
):
    product = product_repository.create(
        Product(
            id=None,
            name="Mechanical Keyboard",
            code="KB-001",
            description="Old description",
            price=250000,
            current_stock=10,
            minimum_stock=3,
            category_id=1,
        )
    )

    updated_product = use_case.execute(
        code="KB-001",
        name="Gaming Keyboard",
        description="Updated description",
        price=280000,
        minimum_stock=5,
    )

    assert updated_product.id == product.id
    assert updated_product.name == "Gaming Keyboard"
    assert updated_product.description == "Updated description"
    assert updated_product.price == 280000
    assert updated_product.minimum_stock == 5

    # category_id was not sent, so it must remain unchanged.
    assert updated_product.category_id == 1

def test_update_product_with_active_category(
    product_repository: FakeProductRepository,
    category_repository: FakeCategoryRepository,
    use_case: UpdateProductUseCase,
):
    product_repository.create(
        Product(
            id=None,
            name="Mechanical Keyboard",
            code="KB-002",
            description="Gaming keyboard",
            price=250000,
            current_stock=10,
            minimum_stock=3,
            category_id=1,
        )
    )

    category_repository.create(
        Category(
            id=None,
            name="Laptops",
            description="Portable computers",
            is_active=True,
        )
    )

    updated_product = use_case.execute(
        code="KB-002",
        category_id=1,
    )

    assert updated_product.category_id == 1

def test_update_product_with_nonexistent_category(
    product_repository: FakeProductRepository,
    use_case: UpdateProductUseCase,
):
    product = product_repository.create(
        Product(
            id=None,
            name="Mechanical Keyboard",
            code="KB-003",
            description="Gaming keyboard",
            price=250000,
            current_stock=10,
            minimum_stock=3,
            category_id=1,
        )
    )

    with pytest.raises(
        ValueError,
        match="Category not found",
    ):
        use_case.execute(
            code="KB-003",
            category_id=999,
        )

    assert product.category_id == 1

def test_update_product_with_inactive_category(
    product_repository: FakeProductRepository,
    category_repository: FakeCategoryRepository,
    use_case: UpdateProductUseCase,
):
    product = product_repository.create(
        Product(
            id=None,
            name="Mechanical Keyboard",
            code="KB-004",
            description="Gaming keyboard",
            price=250000,
            current_stock=10,
            minimum_stock=3,
            category_id=1,
        )
    )

    category_repository.create(
        Category(
            id=None,
            name="Laptops",
            description="Portable computers",
            is_active=False,
        )
    )

    with pytest.raises(
        ValueError,
        match="Category is inactive",
    ):
        use_case.execute(
            code="KB-004",
            category_id=1,
        )

    assert product.category_id == 1
