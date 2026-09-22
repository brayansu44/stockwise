from sqlalchemy import func
from sqlalchemy.orm import Session

from app.domain.entities.category import Category
from app.domain.repositories.category_repository import CategoryRepository
from app.infrastructure.database.models.category_model import CategoryModel


class PostgresCategoryRepository(CategoryRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, category: Category) -> Category:
        category_model = CategoryModel(
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )

        self.db_session.add(category_model)
        self.db_session.commit()
        self.db_session.refresh(category_model)

        return self._to_entity(category_model)

    def get_by_id(self, category_id: int) -> Category | None:
        category_model = (
            self.db_session.query(CategoryModel)
            .filter(CategoryModel.id == category_id)
            .first()
        )

        if not category_model:
            return None

        return self._to_entity(category_model)

    def get_by_name(self, name: str) -> Category | None:
        category_model = (
            self.db_session.query(CategoryModel)
            .filter(
                func.lower(CategoryModel.name) == name.lower()
            )
            .first()
        )

        if not category_model:
            return None

        return self._to_entity(category_model)

    def list_all(self) -> list[Category]:
        categories = self.db_session.query(CategoryModel).all()

        return [
            self._to_entity(category)
            for category in categories
        ]

    def update(self, category: Category) -> Category:
        category_model = (
            self.db_session.query(CategoryModel)
            .filter(CategoryModel.id == category.id)
            .first()
        )

        if not category_model:
            raise ValueError("Category not found")

        category_model.name = category.name
        category_model.description = category.description
        category_model.is_active = category.is_active

        self.db_session.commit()
        self.db_session.refresh(category_model)

        return self._to_entity(category_model)

    def _to_entity(
        self,
        category_model: CategoryModel,
    ) -> Category:
        return Category(
            id=category_model.id,
            name=category_model.name,
            description=category_model.description,
            is_active=category_model.is_active,
        )