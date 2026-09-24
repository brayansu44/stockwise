from app.domain.entities.category import Category
from app.infrastructure.repositories.postgres_category_repository import (
    PostgresCategoryRepository,
)
import pytest

def test_create_category(db_session):
    # Arrange: preparar los datos
    repository = PostgresCategoryRepository(db_session)

    category = Category(
        id=None,
        name="Integration Test Category",
        description="Created during integration testing",
    )

    # Act: ejecutar la operación
    created_category = repository.create(category)

    # Assert: comprobar el resultado
    assert created_category.id is not None
    assert created_category.name == "Integration Test Category"
    assert created_category.description == "Created during integration testing"
    assert created_category.is_active is True

    # Comprobar que realmente se guardó en PostgreSQL
    saved_category = repository.get_by_id(created_category.id)

    assert saved_category is not None
    assert saved_category.id == created_category.id

def test_get_category_by_name_is_case_insensitive(db_session):
    # Arrange
    repository = PostgresCategoryRepository(db_session)

    category = Category(
        id=None,
        name="Electronics",
        description="Electronic products",
    )

    repository.create(category)

    # Act
    result = repository.get_by_name("ELECTRONICS")

    # Assert
    assert result is not None
    assert result.name == "Electronics"
    assert result.description == "Electronic products"

def test_update_category(db_session):
    # Arrange
    repository = PostgresCategoryRepository(db_session)

    category = Category(
        id=None,
        name="Electronics",
        description="Electronic products",
    )

    created_category = repository.create(category)

    # Act
    created_category.name = "Computer Accessories"
    created_category.description = "Keyboards and mice"

    updated_category = repository.update(created_category)

    # Assert
    assert updated_category.id == created_category.id
    assert updated_category.name == "Computer Accessories"
    assert updated_category.description == "Keyboards and mice"

    saved_category = repository.get_by_id(created_category.id)

    assert saved_category is not None
    assert saved_category.name == "Computer Accessories"
    assert saved_category.description == "Keyboards and mice"

def test_update_nonexistent_category(db_session):
    # Arrange
    repository = PostgresCategoryRepository(db_session)

    category = Category(
        id=999999,
        name="Nonexistent Category",
        description="This category does not exist",
    )

    # Act & Assert
    with pytest.raises(ValueError, match="Category not found"):
        repository.update(category)

def test_category_does_not_exist_after_previous_tests(db_session):
    # Arrange
    repository = PostgresCategoryRepository(db_session)

    # Act
    category = repository.get_by_name("Computer Accessories")

    # Assert
    assert category is None


