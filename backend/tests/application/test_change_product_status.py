import pytest

from app.application.use_cases.change_product_status import (
    ChangeProductStatusUseCase,
)
from app.domain.entities.product import Product

from tests.application.test_create_sale import (
    FakeProductRepository,
)


def test_change_product_status_activate():

    product = Product(
        id=1,
        name="Mechanical Keyboard",
        code="KB-001",
        description="Mechanical keyboard for testing",
        price=250000,
        current_stock=8,
        minimum_stock=3,
        category_id=1,
        is_active=False,
    )

    product_repository = FakeProductRepository(
        products=[product]
    )

    use_case = ChangeProductStatusUseCase(
        product_repository=product_repository
    )

    result = use_case.execute(
        code="KB-001",
        is_active=True,
    )

    assert result.is_active is True
    assert product.is_active is True


def test_change_product_status_deactivate():

    product = Product(
        id=1,
        name="Mechanical Keyboard",
        code="KB-001",
        description="Mechanical keyboard for testing",
        price=250000,
        current_stock=8,
        minimum_stock=3,
        category_id=1,
        is_active=True,
    )

    product_repository = FakeProductRepository(
        products=[product]
    )

    use_case = ChangeProductStatusUseCase(
        product_repository=product_repository
    )

    result = use_case.execute(
        code="KB-001",
        is_active=False,
    )

    assert result.is_active is False
    assert product.is_active is False


def test_change_product_status_product_not_found():

    product_repository = FakeProductRepository()

    use_case = ChangeProductStatusUseCase(
        product_repository=product_repository
    )

    with pytest.raises(
        ValueError,
        match="Product not found",
    ):
        use_case.execute(
            code="NOT-EXIST-999",
            is_active=True,
        )