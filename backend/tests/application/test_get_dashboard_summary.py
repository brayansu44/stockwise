from app.application.use_cases.get_dashboard_summary import (
    GetDashboardSummaryUseCase,
)
from app.domain.entities.product import Product
from tests.application.test_create_sale import (
    FakeProductRepository,
    FakeSaleRepository,
)
from app.domain.entities.sale import Sale
from app.domain.entities.sale_item import SaleItem
from app.domain.entities.sale_status import SaleStatus

def test_dashboard_counts_only_active_products():
    products = [
        Product(
            id=1,
            name="Mechanical Keyboard",
            code="KB-001",
            description="Mechanical keyboard",
            price=250000,
            current_stock=10,
            minimum_stock=3,
            is_active=True,
        ),
        Product(
            id=2,
            name="Wireless Mouse",
            code="MOUSE-001",
            description="Wireless mouse",
            price=135000,
            current_stock=5,
            minimum_stock=2,
            is_active=True,
        ),
        Product(
            id=3,
            name="Old Keyboard",
            code="KB-OLD",
            description="Discontinued keyboard",
            price=100000,
            current_stock=1,
            minimum_stock=3,
            is_active=False,
        ),
    ]

    product_repository = FakeProductRepository(products=products)
    sale_repository = FakeSaleRepository()

    use_case = GetDashboardSummaryUseCase(
        product_repository=product_repository,
        sale_repository=sale_repository,
    )

    result = use_case.execute()

    assert result.active_products == 2
    
def test_dashboard_counts_only_active_low_stock_products():
    products = [
        Product(
            id=1,
            name="Mechanical Keyboard",
            code="KB-001",
            description="Mechanical keyboard",
            price=250000,
            current_stock=3,
            minimum_stock=3,
            is_active=True,
        ),
        Product(
            id=2,
            name="Wireless Mouse",
            code="MOUSE-001",
            description="Wireless mouse",
            price=135000,
            current_stock=10,
            minimum_stock=4,
            is_active=True,
        ),
        Product(
            id=3,
            name="Old Keyboard",
            code="KB-OLD",
            description="Discontinued keyboard",
            price=100000,
            current_stock=1,
            minimum_stock=3,
            is_active=False,
        ),
    ]

    product_repository = FakeProductRepository(products=products)
    sale_repository = FakeSaleRepository()

    use_case = GetDashboardSummaryUseCase(
        product_repository=product_repository,
        sale_repository=sale_repository,
    )

    result = use_case.execute()

    assert result.low_stock_products == 1
    
def test_dashboard_counts_only_completed_sales():
    product_repository = FakeProductRepository()
    sale_repository = FakeSaleRepository()

    completed_sale = Sale(
        id=1,
        seller_id=1,
        items=[
            SaleItem(
                product_id=1,
                quantity=2,
                unit_price=100000,
            )
        ],
        status=SaleStatus.COMPLETED,
    )

    cancelled_sale = Sale(
        id=2,
        seller_id=1,
        items=[
            SaleItem(
                product_id=2,
                quantity=1,
                unit_price=150000,
            )
        ],
        status=SaleStatus.CANCELLED,
    )

    sale_repository.sales = [
        completed_sale,
        cancelled_sale,
    ]

    use_case = GetDashboardSummaryUseCase(
        product_repository=product_repository,
        sale_repository=sale_repository,
    )

    result = use_case.execute()

    assert result.completed_sales == 1    

def test_dashboard_sums_amount_only_from_completed_sales():
    product_repository = FakeProductRepository()
    sale_repository = FakeSaleRepository()

    completed_sale_1 = Sale(
        id=1,
        seller_id=1,
        items=[
            SaleItem(
                product_id=1,
                quantity=2,
                unit_price=100000,
            )
        ],
        status=SaleStatus.COMPLETED,
    )

    completed_sale_2 = Sale(
        id=2,
        seller_id=1,
        items=[
            SaleItem(
                product_id=2,
                quantity=1,
                unit_price=150000,
            )
        ],
        status=SaleStatus.COMPLETED,
    )

    cancelled_sale = Sale(
        id=3,
        seller_id=1,
        items=[
            SaleItem(
                product_id=3,
                quantity=5,
                unit_price=50000,
            )
        ],
        status=SaleStatus.CANCELLED,
    )

    sale_repository.sales = [
        completed_sale_1,
        completed_sale_2,
        cancelled_sale,
    ]

    use_case = GetDashboardSummaryUseCase(
        product_repository=product_repository,
        sale_repository=sale_repository,
    )

    result = use_case.execute()

    assert result.total_sales_amount == 350000

def test_dashboard_returns_zero_values_when_there_is_no_data():
    product_repository = FakeProductRepository()
    sale_repository = FakeSaleRepository()

    use_case = GetDashboardSummaryUseCase(
        product_repository=product_repository,
        sale_repository=sale_repository,
    )

    result = use_case.execute()

    assert result.active_products == 0
    assert result.low_stock_products == 0
    assert result.completed_sales == 0
    assert result.total_sales_amount == 0
    
    
