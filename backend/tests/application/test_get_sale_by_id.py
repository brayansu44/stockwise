import pytest

from app.application.use_cases.get_sale_by_id import (
    GetSaleByIdUseCase,
)
from app.domain.entities.sale import Sale
from app.domain.entities.sale_item import SaleItem

from tests.application.test_create_sale import (
    FakeSaleRepository,
)


def test_get_sale_by_id_successfully():

    sale = Sale(
        id=1,
        seller_id=10,
        items=[
            SaleItem(
                product_id=5,
                quantity=2,
                unit_price=100000,
            )
        ],
    )

    sale_repository = FakeSaleRepository()
    sale_repository.sales.append(sale)

    use_case = GetSaleByIdUseCase(
        sale_repository=sale_repository
    )

    result = use_case.execute(1)

    assert result is sale
    assert result.id == 1
    assert result.seller_id == 10
    assert len(result.items) == 1
    assert result.items[0].product_id == 5
    assert result.items[0].quantity == 2


def test_get_sale_by_id_not_found():

    sale_repository = FakeSaleRepository()

    use_case = GetSaleByIdUseCase(
        sale_repository=sale_repository
    )

    with pytest.raises(
        ValueError,
        match="Sale not found",
    ):
        use_case.execute(999)

    
def test_get_sale_by_id_invalid_id():

    sale_repository = FakeSaleRepository()

    use_case = GetSaleByIdUseCase(
        sale_repository=sale_repository
    )

    with pytest.raises(
        ValueError,
        match="Sale ID must be greater than zero",
    ):
        use_case.execute(0)