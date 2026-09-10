from fastapi import APIRouter, Depends, HTTPException, status

from app.application.dto.user_dto import CreateUserRequest, UserResponse
from app.application.mappers.user_mapper import UserMapper
from app.application.use_cases.create_user import CreateUserUseCase
from app.presentation.dependencies.user_dependencies import (
    get_create_user_use_case,
)


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    request: CreateUserRequest,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case),
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