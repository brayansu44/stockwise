import pytest

from app.domain.entities.inventory_movement import InventoryMovement
from app.domain.entities.movement_type import MovementType


def test_entry_movement_is_valid():
    movement = InventoryMovement(
        id=None,
        product_id=1,
        movement_type=MovementType.ENTRY,
        quantity=10,
        reason="Initial stock",
    )

    movement.validate()
    
def test_entry_movement_with_zero_quantity_is_invalid():
    movement = InventoryMovement(
        id=None,
        product_id=1,
        movement_type=MovementType.ENTRY,
        quantity=0,
        reason="Invalid entry",
    )

    with pytest.raises(
        ValueError,
        match="Quantity must be greater than zero",
    ):
        movement.validate()
        
def test_exit_movement_with_zero_quantity_is_invalid():
    movement = InventoryMovement(
        id=None,
        product_id=1,
        movement_type=MovementType.EXIT,
        quantity=0,
        reason="Invalid exit",
    )

    with pytest.raises(
        ValueError,
        match="Quantity must be greater than zero",
    ):
        movement.validate()
        
def test_adjustment_with_negative_quantity_is_invalid():
    movement = InventoryMovement(
        id=None,
        product_id=1,
        movement_type=MovementType.ADJUSTMENT,
        quantity=-1,
        reason="Invalid adjustment",
    )

    with pytest.raises(
        ValueError,
        match="Adjusted stock cannot be negative",
    ):
        movement.validate()
        
def test_adjustment_with_zero_quantity_is_valid():
    movement = InventoryMovement(
        id=None,
        product_id=1,
        movement_type=MovementType.ADJUSTMENT,
        quantity=0,
        reason="Stock adjustment to zero",
    )

    movement.validate()
    
def test_movement_with_invalid_product_id():
    movement = InventoryMovement(
        id=None,
        product_id=0,
        movement_type=MovementType.ENTRY,
        quantity=10,
        reason="Invalid product",
    )

    with pytest.raises(
        ValueError,
        match="Product ID must be greater than zero",
    ):
        movement.validate()
        
def test_movement_with_invalid_sale_id():
    movement = InventoryMovement(
        id=None,
        product_id=1,
        movement_type=MovementType.EXIT,
        quantity=2,
        reason="Sale movement",
        sale_id=0,
    )

    with pytest.raises(
        ValueError,
        match="Sale ID must be greater than zero",
    ):
        movement.validate()