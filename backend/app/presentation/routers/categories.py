from fastapi import APIRouter, Depends, HTTPException, status

from app.application.dto.category_dto import (
    CategoryResponse,
    CreateCategoryRequest,
    UpdateCategoryRequest,
)
from app.application.mappers.category_mapper import CategoryMapper
from app.application.use_cases.create_category import CreateCategoryUseCase
from app.application.use_cases.list_categories import ListCategoriesUseCase
from app.application.use_cases.get_category_by_id import GetCategoryByIdUseCase
from app.application.use_cases.update_category import UpdateCategoryUseCase
from app.application.use_cases.change_category_status import (
    ChangeCategoryStatusUseCase,
)

from app.domain.entities.user_role import UserRole
from app.presentation.dependencies.category_dependencies import (
    get_create_category_use_case,
    get_list_categories_use_case,
    get_category_by_id_use_case,
    get_update_category_use_case,
    get_change_category_status_use_case,
)
from app.presentation.dependencies.role_dependencies import require_roles
from app.domain.entities.user import User
from app.presentation.dependencies.auth_dependencies import get_current_user

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    request: CreateCategoryRequest,
    use_case: CreateCategoryUseCase = Depends(
        get_create_category_use_case
    ),
    _current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.INVENTORY_OPERATOR,
        )
    ),
) -> CategoryResponse:
    try:
        category = CategoryMapper.request_to_entity(request)
        created_category = use_case.execute(category)

        return CategoryMapper.entity_to_response(
            created_category
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "/",
    response_model=list[CategoryResponse],
)
def list_categories(
    use_case: ListCategoriesUseCase = Depends(
        get_list_categories_use_case
    ),
    current_user: User = Depends(get_current_user),
) -> list[CategoryResponse]:
    categories = use_case.execute()

    return [
        CategoryMapper.entity_to_response(category)
        for category in categories
    ]    

@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
)
def get_category_by_id(
    category_id: int,
    use_case: GetCategoryByIdUseCase = Depends(
        get_category_by_id_use_case
    ),
    current_user: User = Depends(get_current_user),
) -> CategoryResponse:
    try:
        category = use_case.execute(category_id)

        return CategoryMapper.entity_to_response(category)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

@router.patch(
    "/{category_id}",
    response_model=CategoryResponse,
)
def update_category(
    category_id: int,
    request: UpdateCategoryRequest,
    use_case: UpdateCategoryUseCase = Depends(
        get_update_category_use_case
    ),
    _current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.INVENTORY_OPERATOR,
        )
    ),
) -> CategoryResponse:
    try:
        updated_category = use_case.execute(
            category_id=category_id,
            name=request.name,
            description=request.description,
        )

        return CategoryMapper.entity_to_response(
            updated_category
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

@router.patch(
    "/{category_id}/activate",
    response_model=CategoryResponse,
)
def activate_category(
    category_id: int,
    use_case: ChangeCategoryStatusUseCase = Depends(
        get_change_category_status_use_case
    ),
    _current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.INVENTORY_OPERATOR,
        )
    ),
) -> CategoryResponse:
    try:
        category = use_case.execute(
            category_id=category_id,
            is_active=True,
        )

        return CategoryMapper.entity_to_response(category)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.patch(
    "/{category_id}/deactivate",
    response_model=CategoryResponse,
)
def deactivate_category(
    category_id: int,
    use_case: ChangeCategoryStatusUseCase = Depends(
        get_change_category_status_use_case
    ),
    _current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.INVENTORY_OPERATOR,
        )
    ),
) -> CategoryResponse:
    try:
        category = use_case.execute(
            category_id=category_id,
            is_active=False,
        )

        return CategoryMapper.entity_to_response(category)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
