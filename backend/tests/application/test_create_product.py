import pytest

from app.application.use_cases.create_product import CreateProductUseCase
from app.domain.entities.product import Product
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
    
@pytest.fixture
def repository() -> FakeProductRepository:
    return FakeProductRepository()

@pytest.fixture
def use_case(
    repository: FakeProductRepository,
) -> CreateProductUseCase:
    return CreateProductUseCase(repository)
    
def test_create_product(
    repository: FakeProductRepository,
    use_case: CreateProductUseCase,
):
    product = Product(
        id=None,
        name="Mechanical Keyboard",
        code="KB-001",
        description="Mechanical keyboard for testing",
        price=250000,
        current_stock=10,
        minimum_stock=3,
    )

    created_product = use_case.execute(product)

    assert created_product.id == 1
    assert created_product.name == "Mechanical Keyboard"
    assert created_product.code == "KB-001"
    assert created_product.price == 250000
    assert created_product.current_stock == 10
    assert len(repository.products) == 1
    
def test_create_product_with_duplicate_code(
    repository: FakeProductRepository,
    use_case: CreateProductUseCase,
):
    existing_product = Product(
        id=None,
        name="Mechanical Keyboard",
        code="KB-001",
        description=None,
        price=250000,
        current_stock=10,
        minimum_stock=3,
    )

    use_case.execute(existing_product)

    duplicate_product = Product(
        id=None,
        name="Another Keyboard",
        code="KB-001",
        description=None,
        price=300000,
        current_stock=5,
        minimum_stock=2,
    )

    with pytest.raises(
        ValueError,
        match="Product code already exists",
    ):
        use_case.execute(duplicate_product)

    assert len(repository.products) == 1
    

def test_create_product_with_negative_price(
    repository: FakeProductRepository,
    use_case: CreateProductUseCase,
):
    product = Product(
        id=None,
        name="Mechanical Keyboard",
        code="KB-001",
        description=None,
        price=-1,
        current_stock=10,
        minimum_stock=3,
    )

    with pytest.raises(
        ValueError,
        match="Product price cannot be negative",
    ):
        use_case.execute(product)

    assert len(repository.products) == 0
    
def test_create_product_with_negative_current_stock(
    repository: FakeProductRepository,
    use_case: CreateProductUseCase,
):
    product = Product(
        id=None,
        name="Mechanical Keyboard",
        code="KB-001",
        description=None,
        price=250000,
        current_stock=-1,
        minimum_stock=3,
    )

    with pytest.raises(
        ValueError,
        match="Current stock cannot be negative",
    ):
        use_case.execute(product)

    assert len(repository.products) == 0
    
def test_create_product_with_negative_minimum_stock(
    repository: FakeProductRepository,
    use_case: CreateProductUseCase,
):
    product = Product(
        id=None,
        name="Mechanical Keyboard",
        code="KB-001",
        description=None,
        price=250000,
        current_stock=10,
        minimum_stock=-1,
    )

    with pytest.raises(
        ValueError,
        match="Minimum stock cannot be negative",
    ):
        use_case.execute(product)

    assert len(repository.products) == 0