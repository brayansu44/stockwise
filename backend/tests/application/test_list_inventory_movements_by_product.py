import pytest

from app.application.use_cases.list_inventory_movements_by_product import (
    ListInventoryMovementsByProductUseCase,
)
from app.domain.entities.inventory_movement import InventoryMovement
from app.domain.entities.movement_type import MovementType
from app.domain.entities.product import Product

from tests.application.test_create_sale import (
    FakeInventoryMovementRepository,
    FakeProductRepository,
)


def test_list_inventory_movements_by_product_successfully():

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

    movement = InventoryMovement(
        id=1,
        product_id=1,
        movement_type=MovementType.ENTRY,
        quantity=10,
        reason="Initial stock",
        sale_id=None,
    )

    product_repository = FakeProductRepository(
        products=[product]
    )

    movement_repository = FakeInventoryMovementRepository()

    movement_repository.movements.append(movement)

    use_case = ListInventoryMovementsByProductUseCase(
        inventory_movement_repository=movement_repository,
        product_repository=product_repository,
    )

    result = use_case.execute("KB-001")

    assert len(result) == 1
    assert result[0] is movement
    assert result[0].product_id == 1
    assert result[0].quantity == 10
    assert result[0].movement_type == MovementType.ENTRY


def test_list_inventory_movements_product_not_found():

    product_repository = FakeProductRepository()
    movement_repository = FakeInventoryMovementRepository()

    use_case = ListInventoryMovementsByProductUseCase(
        inventory_movement_repository=movement_repository,
        product_repository=product_repository,
    )

    with pytest.raises(
        ValueError,
        match="Product not found",
    ):
        use_case.execute("NOT-EXIST-999")


def test_list_inventory_movements_product_id_missing():

    product = Product(
        id=None,
        name="Product Without ID",
        code="NO-ID-001",
        description="Product for testing",
        price=100000,
        current_stock=5,
        minimum_stock=1,
        category_id=1,
    )

    product_repository = FakeProductRepository(
        products=[product]
    )

    movement_repository = FakeInventoryMovementRepository()

    use_case = ListInventoryMovementsByProductUseCase(
        inventory_movement_repository=movement_repository,
        product_repository=product_repository,
    )

    with pytest.raises(
        ValueError,
        match="Product ID is missing",
    ):
        use_case.execute("NO-ID-001")