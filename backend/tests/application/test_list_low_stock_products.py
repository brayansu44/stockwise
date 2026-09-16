from app.application.use_cases.list_low_stock_products import (
    ListLowStockProductsUseCase,
)
from app.domain.entities.product import Product
from tests.application.test_create_sale import FakeProductRepository


def test_list_low_stock_products_successfully():
    products = [
        Product(
            id=1,
            name="Mechanical Keyboard",
            code="KB-001",
            description="Mechanical keyboard",
            price=250000,
            current_stock=3,
            minimum_stock=3,
        ),
        Product(
            id=2,
            name="Wireless Mouse",
            code="MOUSE-001",
            description="Wireless mouse",
            price=135000,
            current_stock=10,
            minimum_stock=4,
        ),
    ]

    product_repository = FakeProductRepository(products=products)

    use_case = ListLowStockProductsUseCase(
        product_repository=product_repository,
    )

    result = use_case.execute()

    assert len(result) == 1
    assert result[0].code == "KB-001"
    assert result[0].current_stock == 3
    assert result[0].minimum_stock == 3
    
def test_list_low_stock_products_returns_empty_list_when_none_are_low():
    products = [
        Product(
            id=1,
            name="Mechanical Keyboard",
            code="KB-001",
            description="Mechanical keyboard",
            price=250000,
            current_stock=10,
            minimum_stock=3,
        ),
        Product(
            id=2,
            name="Wireless Mouse",
            code="MOUSE-001",
            description="Wireless mouse",
            price=135000,
            current_stock=8,
            minimum_stock=4,
        ),
    ]

    product_repository = FakeProductRepository(products=products)

    use_case = ListLowStockProductsUseCase(
        product_repository=product_repository,
    )

    result = use_case.execute()

    assert result == []
    
def test_product_at_minimum_stock_is_considered_low_stock():
    product = Product(
        id=1,
        name="Mechanical Keyboard",
        code="KB-001",
        description="Mechanical keyboard",
        price=250000,
        current_stock=3,
        minimum_stock=3,
    )

    product_repository = FakeProductRepository(products=[product])

    use_case = ListLowStockProductsUseCase(
        product_repository=product_repository,
    )

    result = use_case.execute()

    assert len(result) == 1
    assert result[0].code == "KB-001"
    
def test_inactive_product_is_not_included_in_low_stock_products():
    product = Product(
        id=1,
        name="Discontinued Keyboard",
        code="KB-OLD",
        description="Discontinued product",
        price=200000,
        current_stock=1,
        minimum_stock=3,
        is_active=False,
    )

    product_repository = FakeProductRepository(products=[product])

    use_case = ListLowStockProductsUseCase(
        product_repository=product_repository,
    )

    result = use_case.execute()

    assert result == []