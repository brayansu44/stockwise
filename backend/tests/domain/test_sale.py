import pytest

from app.domain.entities.sale import Sale
from app.domain.entities.sale_item import SaleItem


def test_calculate_sale_total():
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

    assert sale.total == 680000
    
def test_sale_without_items_is_invalid():
    sale = Sale(
        id=1,
        seller_id=1,
        items=[],
    )

    with pytest.raises(
        ValueError,
        match="Sale must contain at least one item",
    ):
        sale.validate()
        
def test_sale_with_invalid_seller_id():
    sale = Sale(
        id=1,
        seller_id=0,
        items=[
            SaleItem(
                product_id=1,
                quantity=1,
                unit_price=250000,
            ),
        ],
    )

    with pytest.raises(
        ValueError,
        match="Seller ID must be greater than zero",
    ):
        sale.validate()
        
def test_sale_with_invalid_item():
    sale = Sale(
        id=1,
        seller_id=1,
        items=[
            SaleItem(
                product_id=1,
                quantity=0,
                unit_price=250000,
            ),
        ],
    )

    with pytest.raises(
        ValueError,
        match="Quantity must be greater than zero",
    ):
        sale.validate()