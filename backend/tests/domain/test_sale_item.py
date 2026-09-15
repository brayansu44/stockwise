import pytest

from app.domain.entities.sale_item import SaleItem


def test_calculate_subtotal():
    item = SaleItem(
        product_id=1,
        quantity=2,
        unit_price=250000,
    )

    assert item.subtotal == 500000
    
def test_sale_item_with_zero_quantity_is_invalid():
    item = SaleItem(
        product_id=1,
        quantity=0,
        unit_price=250000,
    )

    with pytest.raises(
        ValueError,
        match="Quantity must be greater than zero",
    ):
        item.validate()
        
def test_sale_item_with_negative_price_is_invalid():
    item = SaleItem(
        product_id=1,
        quantity=2,
        unit_price=-1,
    )

    with pytest.raises(
        ValueError,
        match="Unit price cannot be negative",
    ):
        item.validate()
        
def test_sale_item_with_invalid_product_id():
    item = SaleItem(
        product_id=0,
        quantity=2,
        unit_price=250000,
    )

    with pytest.raises(
        ValueError,
        match="Product ID must be greater than zero",
    ):
        item.validate()