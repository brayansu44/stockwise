from fastapi import APIRouter, Depends, HTTPException, status

from app.application.dto.user_dto import (
    CreateUserRequest,
    UpdateUserRequest,
    UserResponse,
)
from app.application.mappers.user_mapper import UserMapper
from app.application.use_cases.create_user import CreateUserUseCase
from app.application.use_cases.get_users import GetUsersUseCase
from app.application.use_cases.update_user import UpdateUserUseCase
from app.application.use_cases.change_user_status import ChangeUserStatusUseCase
from app.presentation.dependencies.user_dependencies import (
    get_change_user_status_use_case,
    get_create_user_use_case,
    get_update_user_use_case,
    get_users_use_case,
)
from app.domain.entities.user_role import UserRole
from app.presentation.dependencies.role_dependencies import require_roles


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get(
    "/",
    response_model=list[UserResponse],
)
def get_users(
    use_case: GetUsersUseCase = Depends(get_users_use_case),
    _current_user=Depends(require_roles(UserRole.ADMIN)),
) -> list[UserResponse]:
    users = use_case.execute()

    return [
        UserMapper.entity_to_response(user)
        for user in users
    ]

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    request: CreateUserRequest,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case),
    _current_user=Depends(require_roles(UserRole.ADMIN)),
) -> UserResponse:
    try:
        user = UserMapper.request_to_entity(request)

        created_user = use_case.execute(
            user=user,
            plain_password=request.password,
        )

        return UserMapper.entity_to_response(created_user)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

@router.put(
    "/{user_id}",
    response_model=UserResponse,
)
def update_user(
    user_id: int,
    request: UpdateUserRequest,
    use_case: UpdateUserUseCase = Depends(get_update_user_use_case),
    _current_user=Depends(require_roles(UserRole.ADMIN)),
) -> UserResponse:
    try:
        user = use_case.execute(
            user_id=user_id,
            name=request.name,
            email=request.email,
            role=request.role,
        )

        return UserMapper.entity_to_response(user)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

@router.patch(
    "/{user_id}/deactivate",
    response_model=UserResponse,
)
def deactivate_user(
    user_id: int,
    use_case: ChangeUserStatusUseCase = Depends(get_change_user_status_use_case),
    _current_user=Depends(require_roles(UserRole.ADMIN)),
) -> UserResponse:
    try:
        user = use_case.execute(
            user_id=user_id,
            is_active=False,
        )

        return UserMapper.entity_to_response(user)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

@router.patch(
    "/{user_id}/activate",
    response_model=UserResponse,
)
def activate_user(
    user_id: int,
    use_case: ChangeUserStatusUseCase = Depends(get_change_user_status_use_case),
    _current_user=Depends(require_roles(UserRole.ADMIN)),
) -> UserResponse:
    try:
        user = use_case.execute(
            user_id=user_id,
            is_active=True,
        )

        return UserMapper.entity_to_response(user)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
