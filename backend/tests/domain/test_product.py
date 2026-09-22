import pytest

from app.domain.entities.product import Product

@pytest.fixture
def product() -> Product:
    return Product(
        id=1,
        name="Test Product",
        code="TEST-001",
        description="Product for unit testing",
        price=10000,
        current_stock=10,
        minimum_stock=3,
        category_id=1,
    )

def test_increase_stock(product: Product):
    product.increase_stock(5)

    assert product.current_stock == 15
    
def test_decrease_stock_with_insufficient_stock(product: Product):
    with pytest.raises(ValueError, match="Insufficient stock"):
        product.decrease_stock(11)

    assert product.current_stock == 10

def test_increase_stock_with_invalid_quantity(product: Product):
    with pytest.raises(
        ValueError,
        match="Quantity must be greater than zero",
    ):
        product.increase_stock(0)

    assert product.current_stock == 10

def test_product_is_low_stock(product: Product):
    product.current_stock = 3

    assert product.is_low_stock() is True
    
def test_decrease_stock_with_invalid_quantity(product: Product):
    with pytest.raises(
        ValueError,
        match="Quantity must be greater than zero",
    ):
        product.decrease_stock(0)

    assert product.current_stock == 10
    
def test_product_is_not_low_stock(product: Product):
    assert product.is_low_stock() is False