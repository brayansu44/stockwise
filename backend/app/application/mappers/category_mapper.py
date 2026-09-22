from app.application.dto.category_dto import (
    CategoryResponse,
    CreateCategoryRequest,
)
from app.domain.entities.category import Category


class CategoryMapper:
    @staticmethod
    def request_to_entity(
        request: CreateCategoryRequest,
    ) -> Category:
        return Category(
            id=None,
            name=request.name,
            description=request.description,
        )

    @staticmethod
    def entity_to_response(
        category: Category,
    ) -> CategoryResponse:
        if category.id is None:
            raise ValueError(
                "Category must have an ID before creating a response"
            )

        return CategoryResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )