import pytest

from app.application.use_cases.create_sale import CreateSaleUseCase
from app.domain.entities.product import Product
from app.domain.entities.sale import Sale
from app.domain.entities.inventory_movement import InventoryMovement
from app.domain.repositories.product_repository import ProductRepository
from app.domain.repositories.sale_repository import SaleRepository
from app.domain.repositories.inventory_movement_repository import (
    InventoryMovementRepository,
)
from app.application.dto.sale_dto import CreateSaleItemRequest
from app.domain.entities.movement_type import MovementType
from app.domain.unit_of_work import UnitOfWork
class FakeProductRepository(ProductRepository):
    def __init__(self, products: list[Product] | None = None):
        self.products = products or []

    def create(self, product: Product) -> Product:
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
    
class FakeSaleRepository(SaleRepository):
    def __init__(self):
        self.sales: list[Sale] = []
        self.committed = False

    def create(self, sale: Sale) -> Sale:
        sale.id = len(self.sales) + 1
        self.sales.append(sale)
        self.committed = True
        return sale

    def create_without_commit(self, sale: Sale) -> Sale:
        sale.id = len(self.sales) + 1
        self.sales.append(sale)
        return sale

    def get_by_id(self, sale_id: int) -> Sale | None:
        for sale in self.sales:
            if sale.id == sale_id:
                return sale

        return None

    def list_all(self) -> list[Sale]:
        return self.sales

    def update_without_commit(self, sale: Sale) -> Sale:
        return sale

    def commit(self) -> None:
        self.committed = True
        
class FakeInventoryMovementRepository(InventoryMovementRepository):
    def __init__(self):
        self.movements: list[InventoryMovement] = []

    def create(
        self,
        movement: InventoryMovement,
    ) -> InventoryMovement:
        movement.id = len(self.movements) + 1
        self.movements.append(movement)
        return movement

    def create_without_commit(
        self,
        movement: InventoryMovement,
    ) -> InventoryMovement:
        movement.id = len(self.movements) + 1
        self.movements.append(movement)
        return movement

    def list_by_product(
        self,
        product_id: int,
    ) -> list[InventoryMovement]:
        return [
            movement
            for movement in self.movements
            if movement.product_id == product_id
        ]

class FakeUnitOfWork(UnitOfWork):
    def __init__(self):
        self.committed = False
        self.rolled_back = False

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.rolled_back = True

@pytest.fixture
def product_repository() -> FakeProductRepository:
    keyboard = Product(
        id=1,
        name="Mechanical Keyboard",
        code="KB-001",
        description="Mechanical keyboard for testing",
        price=250000,
        current_stock=10,
        minimum_stock=3,
        category_id=1,
    )

    hub = Product(
        id=2,
        name="USB-C Hub",
        code="HUB-001",
        description="USB-C hub for testing",
        price=180000,
        current_stock=2,
        minimum_stock=1,
        category_id=1,
    )

    return FakeProductRepository(
        products=[keyboard, hub]
    )

@pytest.fixture
def sale_repository() -> FakeSaleRepository:
    return FakeSaleRepository()


@pytest.fixture
def movement_repository() -> FakeInventoryMovementRepository:
    return FakeInventoryMovementRepository()


@pytest.fixture
def unit_of_work() -> FakeUnitOfWork:
    return FakeUnitOfWork()

@pytest.fixture
def use_case(
    sale_repository: FakeSaleRepository,
    product_repository: FakeProductRepository,
    movement_repository: FakeInventoryMovementRepository,
    unit_of_work: FakeUnitOfWork,
) -> CreateSaleUseCase:
    return CreateSaleUseCase(
        sale_repository=sale_repository,
        product_repository=product_repository,
        inventory_movement_repository=movement_repository,
        unit_of_work=unit_of_work,
    )
    
def test_create_sale_successfully(
    use_case: CreateSaleUseCase,
    product_repository: FakeProductRepository,
    sale_repository: FakeSaleRepository,
    movement_repository: FakeInventoryMovementRepository,
    unit_of_work: FakeUnitOfWork,
):
    items = [
        CreateSaleItemRequest(
            product_code="KB-001",
            quantity=2,
        )
    ]

    sale = use_case.execute(
        seller_id=1,
        items=items,
    )

    product = product_repository.get_by_code("KB-001")

    assert sale.id == 1
    assert sale.seller_id == 1
    assert sale.total == 500000

    assert product is not None
    assert product.current_stock == 8

    assert len(sale_repository.sales) == 1
    assert len(movement_repository.movements) == 1

    movement = movement_repository.movements[0]
    
    assert movement.movement_type == MovementType.EXIT

    assert movement.product_id == 1
    assert movement.quantity == 2
    assert movement.sale_id == 1
    assert movement.reason == "Sale #1"

    assert unit_of_work.committed is True
    assert unit_of_work.rolled_back is False
    
def test_create_sale_with_invalid_seller_id(
    use_case: CreateSaleUseCase,
    product_repository: FakeProductRepository,
    sale_repository: FakeSaleRepository,
    movement_repository: FakeInventoryMovementRepository,
):
    items = [
        CreateSaleItemRequest(
            product_code="KB-001",
            quantity=2,
        )
    ]

    with pytest.raises(
        ValueError,
        match="Seller ID must be greater than zero",
    ):
        use_case.execute(
            seller_id=0,
            items=items,
        )

    product = product_repository.get_by_code("KB-001")

    assert product is not None
    assert product.current_stock == 10
    assert len(sale_repository.sales) == 0
    assert len(movement_repository.movements) == 0
    assert sale_repository.committed is False
    
def test_create_sale_without_items(
    use_case: CreateSaleUseCase,
    product_repository: FakeProductRepository,
    sale_repository: FakeSaleRepository,
    movement_repository: FakeInventoryMovementRepository,
):
    with pytest.raises(
        ValueError,
        match="Sale must contain at least one item",
    ):
        use_case.execute(
            seller_id=1,
            items=[],
        )

    product = product_repository.get_by_code("KB-001")

    assert product is not None
    assert product.current_stock == 10
    assert len(sale_repository.sales) == 0
    assert len(movement_repository.movements) == 0
    assert sale_repository.committed is False
    
def test_create_sale_with_product_not_found(
    use_case: CreateSaleUseCase,
    product_repository: FakeProductRepository,
    sale_repository: FakeSaleRepository,
    movement_repository: FakeInventoryMovementRepository,
):
    items = [
        CreateSaleItemRequest(
            product_code="NOT-FOUND",
            quantity=2,
        )
    ]

    with pytest.raises(
        ValueError,
        match="Product not found: NOT-FOUND",
    ):
        use_case.execute(
            seller_id=1,
            items=items,
        )

    product = product_repository.get_by_code("KB-001")

    assert product is not None
    assert product.current_stock == 10
    assert len(sale_repository.sales) == 0
    assert len(movement_repository.movements) == 0
    assert sale_repository.committed is False
    
def test_create_sale_with_inactive_product(
    use_case: CreateSaleUseCase,
    product_repository: FakeProductRepository,
    sale_repository: FakeSaleRepository,
    movement_repository: FakeInventoryMovementRepository,
):
    product = product_repository.get_by_code("KB-001")

    assert product is not None
    product.is_active = False

    items = [
        CreateSaleItemRequest(
            product_code="KB-001",
            quantity=2,
        )
    ]

    with pytest.raises(
        ValueError,
        match="Product is inactive: KB-001",
    ):
        use_case.execute(
            seller_id=1,
            items=items,
        )

    assert product.current_stock == 10
    assert len(sale_repository.sales) == 0
    assert len(movement_repository.movements) == 0
    assert sale_repository.committed is False
    
def test_create_sale_with_insufficient_stock(
    use_case: CreateSaleUseCase,
    product_repository: FakeProductRepository,
    sale_repository: FakeSaleRepository,
    movement_repository: FakeInventoryMovementRepository,
):
    items = [
        CreateSaleItemRequest(
            product_code="KB-001",
            quantity=11,
        )
    ]

    with pytest.raises(
        ValueError,
        match="Insufficient stock",
    ):
        use_case.execute(
            seller_id=1,
            items=items,
        )

    product = product_repository.get_by_code("KB-001")

    assert product is not None
    assert product.current_stock == 10
    assert len(sale_repository.sales) == 0
    assert len(movement_repository.movements) == 0
    assert sale_repository.committed is False
    
def test_create_sale_with_duplicate_product(
    use_case: CreateSaleUseCase,
    product_repository: FakeProductRepository,
    sale_repository: FakeSaleRepository,
    movement_repository: FakeInventoryMovementRepository,
):
    items = [
        CreateSaleItemRequest(
            product_code="KB-001",
            quantity=2,
        ),
        CreateSaleItemRequest(
            product_code="KB-001",
            quantity=1,
        ),
    ]

    with pytest.raises(
        ValueError,
        match="Duplicate product in sale: KB-001",
    ):
        use_case.execute(
            seller_id=1,
            items=items,
        )

    product = product_repository.get_by_code("KB-001")

    assert product is not None
    assert product.current_stock == 10
    assert len(sale_repository.sales) == 0
    assert len(movement_repository.movements) == 0
    assert sale_repository.committed is False
    
def test_create_sale_with_insufficient_stock_in_second_product(
    use_case: CreateSaleUseCase,
    product_repository: FakeProductRepository,
    sale_repository: FakeSaleRepository,
    movement_repository: FakeInventoryMovementRepository,
):
    items = [
        CreateSaleItemRequest(
            product_code="KB-001",
            quantity=2,
        ),
        CreateSaleItemRequest(
            product_code="HUB-001",
            quantity=3,
        ),
    ]

    with pytest.raises(
        ValueError,
        match="Insufficient stock",
    ):
        use_case.execute(
            seller_id=1,
            items=items,
        )

    keyboard = product_repository.get_by_code("KB-001")
    hub = product_repository.get_by_code("HUB-001")

    assert keyboard is not None
    assert hub is not None
    
    assert keyboard.current_stock == 10
    assert hub.current_stock == 2

    assert len(sale_repository.sales) == 0
    assert len(movement_repository.movements) == 0
    assert sale_repository.committed is False

def test_create_sale_rolls_back_when_movement_fails(
    use_case: CreateSaleUseCase,
    unit_of_work: FakeUnitOfWork,
    movement_repository: FakeInventoryMovementRepository,
    monkeypatch,
):
    items = [
        CreateSaleItemRequest(
            product_code="KB-001",
            quantity=2,
        )
    ]

    def simulate_failure(movement):
        raise RuntimeError("Database error")

    monkeypatch.setattr(
        movement_repository,
        "create_without_commit",
        simulate_failure,
    )

    with pytest.raises(RuntimeError, match="Database error"):
        use_case.execute(
            seller_id=1,
            items=items,
        )

    assert unit_of_work.committed is False
    assert unit_of_work.rolled_back is True

def test_create_sale_with_product_without_id(
    use_case: CreateSaleUseCase,
    product_repository: FakeProductRepository,
    sale_repository: FakeSaleRepository,
    movement_repository: FakeInventoryMovementRepository,
    unit_of_work: FakeUnitOfWork,
):
    product = product_repository.get_by_code("KB-001")

    assert product is not None
    product.id = None

    items = [
        CreateSaleItemRequest(
            product_code="KB-001",
            quantity=2,
        )
    ]

    with pytest.raises(
        ValueError,
        match="Product ID is missing: KB-001",
    ):
        use_case.execute(
            seller_id=1,
            items=items,
        )

    assert product.current_stock == 10
    assert len(sale_repository.sales) == 0
    assert len(movement_repository.movements) == 0
    assert unit_of_work.committed is False

def test_create_sale_without_generated_id(
    use_case: CreateSaleUseCase,
    sale_repository: FakeSaleRepository,
    product_repository: FakeProductRepository,
    movement_repository: FakeInventoryMovementRepository,
    unit_of_work: FakeUnitOfWork,
    monkeypatch,
):
    def simulate_missing_sale_id(sale):
        return sale

    monkeypatch.setattr(
        sale_repository,
        "create_without_commit",
        simulate_missing_sale_id,
    )

    items = [
        CreateSaleItemRequest(
            product_code="KB-001",
            quantity=2,
        )
    ]

    with pytest.raises(
        ValueError,
        match="Sale ID was not generated",
    ):
        use_case.execute(
            seller_id=1,
            items=items,
        )

    assert unit_of_work.rolled_back is True
    assert unit_of_work.committed is False
    assert len(movement_repository.movements) == 0
