from app.domain.entities.category import Category
import pytest

def test_category_can_be_created():
    category = Category(
        id=1,
        name="Peripherals",
        description="Computer peripherals",
        is_active=True,
    )

    assert category.id == 1
    assert category.name == "Peripherals"
    assert category.description == "Computer peripherals"
    assert category.is_active is True
    
def test_category_name_cannot_be_empty():
    with pytest.raises(
        ValueError,
        match="Category name cannot be empty",
    ):
        Category(
            id=1,
            name="",
            description="Invalid category",
        )
    
def test_category_name_cannot_contain_only_whitespace():
    with pytest.raises(
        ValueError,
        match="Category name cannot be empty",
    ):
        Category(
            id=1,
            name="   ",
            description="Invalid category",
        )
        
def test_category_name_is_trimmed():
    category = Category(
        id=1,
        name="  Peripherals  ",
        description="Computer peripherals",
    )

    assert category.name == "Peripherals"        

