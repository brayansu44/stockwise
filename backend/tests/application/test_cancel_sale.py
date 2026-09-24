import pytest

from app.application.use_cases.cancel_sale import CancelSaleUseCase
from app.domain.entities.product import Product
from app.domain.entities.sale import Sale
from app.domain.entities.sale_item import SaleItem
from app.domain.entities.sale_status import SaleStatus


from tests.application.test_create_sale import (
    FakeInventoryMovementRepository,
    FakeProductRepository,
    FakeSaleRepository,
)


class FakeUnitOfWork:

    def __init__(self):
        self.committed = False
        self.rolled_back = False

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.rolled_back = True


def test_cancel_sale_successfully():

    product = Product(
        id=1,
        name="Mechanical Keyboard",
        code="KB-001",
        description="Mechanical keyboard for testing",
        price=250000,
        current_stock=8,
        minimum_stock=3,
        category_id=1,
    )

    sale = Sale(
        id=1,
        seller_id=1,
        items=[
            SaleItem(
                product_id=1,
                quantity=2,
                unit_price=250000,
            )
        ],
    )

    product_repository = FakeProductRepository(
        products=[product]
    )

    sale_repository = FakeSaleRepository()
    sale_repository.sales.append(sale)

    movement_repository = FakeInventoryMovementRepository()

    unit_of_work = FakeUnitOfWork()

    use_case = CancelSaleUseCase(
        sale_repository=sale_repository,
        product_repository=product_repository,
        inventory_movement_repository=movement_repository,
        unit_of_work=unit_of_work,
    )

    result = use_case.execute(1)

    assert result.status == SaleStatus.CANCELLED
    assert product.current_stock == 10

    assert len(movement_repository.movements) == 1

    movement = movement_repository.movements[0]

    assert movement.product_id == 1
    assert movement.quantity == 2
    assert movement.sale_id == 1
    assert movement.reason == "Sale cancellation #1"

    assert unit_of_work.committed is True
    assert unit_of_work.rolled_back is False


def test_cancel_sale_already_cancelled():

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

    sale = Sale(
        id=1,
        seller_id=1,
        items=[
            SaleItem(
                product_id=1,
                quantity=2,
                unit_price=250000,
            )
        ],
        status=SaleStatus.CANCELLED,
    )

    product_repository = FakeProductRepository(
        products=[product]
    )

    sale_repository = FakeSaleRepository()
    sale_repository.sales.append(sale)

    movement_repository = FakeInventoryMovementRepository()

    unit_of_work = FakeUnitOfWork()

    use_case = CancelSaleUseCase(
        sale_repository=sale_repository,
        product_repository=product_repository,
        inventory_movement_repository=movement_repository,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(
        ValueError,
        match="Sale is already cancelled",
    ):
        use_case.execute(1)

    assert product.current_stock == 10
    assert len(movement_repository.movements) == 0

    assert sale_repository.committed is False
    assert unit_of_work.committed is False
    assert unit_of_work.rolled_back is False


def test_cancel_sale_not_found():

    product_repository = FakeProductRepository()
    sale_repository = FakeSaleRepository()
    movement_repository = FakeInventoryMovementRepository()

    unit_of_work = FakeUnitOfWork()

    use_case = CancelSaleUseCase(
        sale_repository=sale_repository,
        product_repository=product_repository,
        inventory_movement_repository=movement_repository,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(
        ValueError,
        match="Sale not found",
    ):
        use_case.execute(999)

    assert len(movement_repository.movements) == 0
    assert sale_repository.committed is False

    assert unit_of_work.committed is False
    assert unit_of_work.rolled_back is False


def test_cancel_sale_does_not_modify_stock_when_second_product_is_not_found():

    keyboard = Product(
        id=1,
        name="Mechanical Keyboard",
        code="KB-001",
        description="Mechanical keyboard for testing",
        price=250000,
        current_stock=8,
        minimum_stock=3,
        category_id=1,
    )

    sale = Sale(
        id=1,
        seller_id=1,
        items=[
            SaleItem(
                product_id=1,
                quantity=2,
                unit_price=250000,
            ),
            SaleItem(
                product_id=999,
                quantity=1,
                unit_price=180000,
            ),
        ],
    )

    product_repository = FakeProductRepository(
        products=[keyboard]
    )

    sale_repository = FakeSaleRepository()
    sale_repository.sales.append(sale)

    movement_repository = FakeInventoryMovementRepository()

    unit_of_work = FakeUnitOfWork()

    use_case = CancelSaleUseCase(
        sale_repository=sale_repository,
        product_repository=product_repository,
        inventory_movement_repository=movement_repository,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(
        ValueError,
        match="Product not found for sale item: 999",
    ):
        use_case.execute(1)

    assert keyboard.current_stock == 8
    assert len(movement_repository.movements) == 0

    assert sale.status == SaleStatus.COMPLETED
    assert sale_repository.committed is False

    assert unit_of_work.committed is False
    assert unit_of_work.rolled_back is False


def test_cancel_sale_with_invalid_id():

    product_repository = FakeProductRepository()
    sale_repository = FakeSaleRepository()
    movement_repository = FakeInventoryMovementRepository()

    unit_of_work = FakeUnitOfWork()

    use_case = CancelSaleUseCase(
        sale_repository=sale_repository,
        product_repository=product_repository,
        inventory_movement_repository=movement_repository,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(
        ValueError,
        match="Sale ID must be greater than zero",
    ):
        use_case.execute(0)

    assert len(movement_repository.movements) == 0
    assert sale_repository.committed is False

    assert unit_of_work.committed is False
    assert unit_of_work.rolled_back is False


def test_cancel_sale_with_multiple_products():

    keyboard = Product(
        id=1,
        name="Mechanical Keyboard",
        code="KB-001",
        description="Mechanical keyboard for testing",
        price=250000,
        current_stock=8,
        minimum_stock=3,
        category_id=1,
    )

    hub = Product(
        id=2,
        name="USB-C Hub",
        code="HUB-001",
        description="USB-C hub for testing",
        price=180000,
        current_stock=1,
        minimum_stock=1,
        category_id=1,
    )

    sale = Sale(
        id=1,
        seller_id=1,
        items=[
            SaleItem(
                product_id=1,
                quantity=2,
                unit_price=250000,
            ),
            SaleItem(
                product_id=2,
                quantity=1,
                unit_price=180000,
            ),
        ],
    )

    product_repository = FakeProductRepository(
        products=[keyboard, hub]
    )

    sale_repository = FakeSaleRepository()
    sale_repository.sales.append(sale)

    movement_repository = FakeInventoryMovementRepository()

    unit_of_work = FakeUnitOfWork()

    use_case = CancelSaleUseCase(
        sale_repository=sale_repository,
        product_repository=product_repository,
        inventory_movement_repository=movement_repository,
        unit_of_work=unit_of_work,
    )

    result = use_case.execute(1)

    assert result.status == SaleStatus.CANCELLED

    assert keyboard.current_stock == 10
    assert hub.current_stock == 2

    assert len(movement_repository.movements) == 2

    assert movement_repository.movements[0].product_id == 1
    assert movement_repository.movements[0].quantity == 2
    assert movement_repository.movements[0].sale_id == 1

    assert movement_repository.movements[1].product_id == 2
    assert movement_repository.movements[1].quantity == 1
    assert movement_repository.movements[1].sale_id == 1

    assert unit_of_work.committed is True
    assert unit_of_work.rolled_back is False

def test_cancel_sale_rolls_back_when_movement_fails(
    monkeypatch,
):
    product = Product(
        id=1,
        name="Mechanical Keyboard",
        code="KB-001",
        description="Keyboard for rollback testing",
        price=250000,
        current_stock=8,
        minimum_stock=3,
        category_id=1,
    )

    sale = Sale(
        id=1,
        seller_id=1,
        items=[
            SaleItem(
                product_id=1,
                quantity=2,
                unit_price=250000,
            )
        ],
    )

    product_repository = FakeProductRepository(
        products=[product]
    )

    sale_repository = FakeSaleRepository()
    sale_repository.sales.append(sale)

    movement_repository = FakeInventoryMovementRepository()
    unit_of_work = FakeUnitOfWork()

    def simulate_database_error(movement):
        raise RuntimeError("Simulated database error")

    monkeypatch.setattr(
        movement_repository,
        "create_without_commit",
        simulate_database_error,
    )

    use_case = CancelSaleUseCase(
        sale_repository=sale_repository,
        product_repository=product_repository,
        inventory_movement_repository=movement_repository,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(
        RuntimeError,
        match="Simulated database error",
    ):
        use_case.execute(1)

    assert unit_of_work.rolled_back is True
    assert unit_of_work.committed is False
