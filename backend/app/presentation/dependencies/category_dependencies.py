from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.use_cases.create_category import CreateCategoryUseCase
from app.application.use_cases.list_categories import ListCategoriesUseCase
from app.infrastructure.repositories.postgres_category_repository import (
    PostgresCategoryRepository,
)
from app.presentation.dependencies.database_dependencies import (
    get_db_session,
)
from app.application.use_cases.get_category_by_id import GetCategoryByIdUseCase
from app.application.use_cases.update_category import UpdateCategoryUseCase
from app.application.use_cases.change_category_status import (
    ChangeCategoryStatusUseCase,
)

def get_category_repository(
    db_session: Session = Depends(get_db_session),
) -> PostgresCategoryRepository:
    return PostgresCategoryRepository(db_session)


def get_create_category_use_case(
    category_repository: PostgresCategoryRepository = Depends(
        get_category_repository
    ),
) -> CreateCategoryUseCase:
    return CreateCategoryUseCase(category_repository)


def get_list_categories_use_case(
    category_repository: PostgresCategoryRepository = Depends(
        get_category_repository
    ),
) -> ListCategoriesUseCase:
    return ListCategoriesUseCase(category_repository)

def get_category_by_id_use_case(
    category_repository: PostgresCategoryRepository = Depends(
        get_category_repository
    ),
) -> GetCategoryByIdUseCase:
    return GetCategoryByIdUseCase(category_repository)

def get_update_category_use_case(
    category_repository: PostgresCategoryRepository = Depends(
        get_category_repository
    ),
) -> UpdateCategoryUseCase:
    return UpdateCategoryUseCase(category_repository)

def get_change_category_status_use_case(
    category_repository: PostgresCategoryRepository = Depends(
        get_category_repository
    ),
) -> ChangeCategoryStatusUseCase:
    return ChangeCategoryStatusUseCase(category_repository)