import pytest

from app.application.use_cases.create_inventory_movement import (
    CreateInventoryMovementUseCase,
)
from app.domain.entities.product import Product
from app.domain.entities.movement_type import MovementType

from tests.application.test_create_sale import (
    FakeInventoryMovementRepository,
    FakeProductRepository,
)

from app.domain.unit_of_work import UnitOfWork

class FailingInventoryMovementRepository(
    FakeInventoryMovementRepository
):
    def create_without_commit(self, movement):
        raise RuntimeError("Database error")

class FakeUnitOfWork(UnitOfWork):
    def __init__(self):
        self.committed = False
        self.rolled_back = False

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.rolled_back = True

def test_create_inventory_entry_successfully():
    product = Product(
        id=1,
        name="Mechanical Keyboard",
        code="KB-001",
        description="Mechanical keyboard for testing",
        price=250000,
        current_stock=10,
        minimum_stock=3,
        category_id=1,
    )

    product_repository = FakeProductRepository(products=[product])
    movement_repository = FakeInventoryMovementRepository()
    
    unit_of_work = FakeUnitOfWork()

    use_case = CreateInventoryMovementUseCase(
        inventory_movement_repository=movement_repository,
        product_repository=product_repository,
        unit_of_work=unit_of_work,
    )

    result = use_case.execute(
        product_code="KB-001",
        movement_type=MovementType.ENTRY,
        quantity=5,
        reason="Supplier purchase",
    )

    assert product.current_stock == 15

    assert result.id == 1
    assert result.product_id == 1
    assert result.movement_type == MovementType.ENTRY
    assert result.quantity == 5
    assert result.reason == "Supplier purchase"

    assert len(movement_repository.movements) == 1
    
    assert unit_of_work.committed is True
    assert unit_of_work.rolled_back is False
    
def test_create_inventory_exit_successfully():
    product = Product(
        id=1,
        name="Mechanical Keyboard",
        code="KB-001",
        description="Mechanical keyboard for testing",
        price=250000,
        current_stock=10,
        minimum_stock=3,
        category_id=1,
    )

    product_repository = FakeProductRepository(products=[product])
    movement_repository = FakeInventoryMovementRepository()
    
    unit_of_work = FakeUnitOfWork()

    use_case = CreateInventoryMovementUseCase(
        inventory_movement_repository=movement_repository,
        product_repository=product_repository,
        unit_of_work=unit_of_work,
    )

    result = use_case.execute(
        product_code="KB-001",
        movement_type=MovementType.EXIT,
        quantity=4,
        reason="Damaged units",
    )

    assert product.current_stock == 6

    assert result.id == 1
    assert result.product_id == 1
    assert result.movement_type == MovementType.EXIT
    assert result.quantity == 4
    assert result.reason == "Damaged units"

    assert len(movement_repository.movements) == 1
    
def test_create_inventory_adjustment_successfully():
    product = Product(
        id=1,
        name="Mechanical Keyboard",
        code="KB-001",
        description="Mechanical keyboard for testing",
        price=250000,
        current_stock=10,
        minimum_stock=3,
        category_id=1,
    )

    product_repository = FakeProductRepository(products=[product])
    movement_repository = FakeInventoryMovementRepository()
    
    unit_of_work = FakeUnitOfWork()

    use_case = CreateInventoryMovementUseCase(
        inventory_movement_repository=movement_repository,
        product_repository=product_repository,
        unit_of_work=unit_of_work,
    )

    result = use_case.execute(
        product_code="KB-001",
        movement_type=MovementType.ADJUSTMENT,
        quantity=7,
        reason="Physical inventory count",
    )

    assert product.current_stock == 7

    assert result.id == 1
    assert result.product_id == 1
    assert result.movement_type == MovementType.ADJUSTMENT
    assert result.quantity == 7
    assert result.reason == "Physical inventory count"

    assert len(movement_repository.movements) == 1
    
def test_create_inventory_movement_product_not_found():
    product_repository = FakeProductRepository()
    movement_repository = FakeInventoryMovementRepository()
    
    unit_of_work = FakeUnitOfWork()

    use_case = CreateInventoryMovementUseCase(
        inventory_movement_repository=movement_repository,
        product_repository=product_repository,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(ValueError, match="Product not found"):
        use_case.execute(
            product_code="NOT-FOUND",
            movement_type=MovementType.ENTRY,
            quantity=5,
            reason="Supplier purchase",
        )

    assert len(movement_repository.movements) == 0
    
def test_create_inventory_movement_with_inactive_product():
    product = Product(
        id=1,
        name="Mechanical Keyboard",
        code="KB-001",
        description="Mechanical keyboard for testing",
        price=250000,
        current_stock=10,
        minimum_stock=3,
        is_active=False,
        category_id=1,
    )

    product_repository = FakeProductRepository(products=[product])
    movement_repository = FakeInventoryMovementRepository()
    
    unit_of_work = FakeUnitOfWork()

    use_case = CreateInventoryMovementUseCase(
        inventory_movement_repository=movement_repository,
        product_repository=product_repository,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(ValueError, match="Product is inactive"):
        use_case.execute(
            product_code="KB-001",
            movement_type=MovementType.ENTRY,
            quantity=5,
            reason="Supplier purchase",
        )

    assert product.current_stock == 10
    assert len(movement_repository.movements) == 0
    
def test_create_inventory_exit_with_insufficient_stock():
    product = Product(
        id=1,
        name="Mechanical Keyboard",
        code="KB-001",
        description="Mechanical keyboard for testing",
        price=250000,
        current_stock=10,
        minimum_stock=3,
        category_id=1,
    )

    product_repository = FakeProductRepository(products=[product])
    movement_repository = FakeInventoryMovementRepository()
    
    unit_of_work = FakeUnitOfWork()

    use_case = CreateInventoryMovementUseCase(
        inventory_movement_repository=movement_repository,
        product_repository=product_repository,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(ValueError, match="Insufficient stock"):
        use_case.execute(
            product_code="KB-001",
            movement_type=MovementType.EXIT,
            quantity=11,
            reason="Damaged units",
        )

    assert product.current_stock == 10
    assert len(movement_repository.movements) == 0
    
def test_create_inventory_adjustment_with_negative_stock():
    product = Product(
        id=1,
        name="Mechanical Keyboard",
        code="KB-001",
        description="Mechanical keyboard for testing",
        price=250000,
        current_stock=10,
        minimum_stock=3,
        category_id=1,
    )

    product_repository = FakeProductRepository(products=[product])
    movement_repository = FakeInventoryMovementRepository()
    
    unit_of_work = FakeUnitOfWork()

    use_case = CreateInventoryMovementUseCase(
        inventory_movement_repository=movement_repository,
        product_repository=product_repository,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(
        ValueError,
        match="Adjusted stock cannot be negative",
    ):
        use_case.execute(
            product_code="KB-001",
            movement_type=MovementType.ADJUSTMENT,
            quantity=-1,
            reason="Physical inventory correction",
        )

    assert product.current_stock == 10
    assert len(movement_repository.movements) == 0
    
def test_inventory_stock_is_not_left_modified_when_movement_creation_fails():
    product = Product(
        id=1,
        name="Mechanical Keyboard",
        code="KB-001",
        description="Mechanical keyboard for testing",
        price=250000,
        current_stock=10,
        minimum_stock=3,
        category_id=1,
    )

    product_repository = FakeProductRepository(products=[product])
    movement_repository = FailingInventoryMovementRepository()
    
    unit_of_work = FakeUnitOfWork()

    use_case = CreateInventoryMovementUseCase(
        inventory_movement_repository=movement_repository,
        product_repository=product_repository,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(RuntimeError, match="Database error"):
        use_case.execute(
            product_code="KB-001",
            movement_type=MovementType.ENTRY,
            quantity=5,
            reason="Supplier purchase",
        )

    assert unit_of_work.rolled_back is True
    assert unit_of_work.committed is False
    assert len(movement_repository.movements) == 0