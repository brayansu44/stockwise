import pytest

from app.application.mappers.category_mapper import CategoryMapper
from app.domain.entities.category import Category


def test_entity_to_response_without_id():
    category = Category(
        id=None,
        name="Electronics",
        description="Electronic products",
    )

    with pytest.raises(
        ValueError,
        match="Category must have an ID before creating a response",
    ):
        CategoryMapper.entity_to_response(category)