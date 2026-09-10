from fastapi import APIRouter, Depends, HTTPException, status

from app.application.dto.user_dto import LoginRequest, TokenResponse
from app.application.use_cases.login_user import LoginUserUseCase
from app.presentation.dependencies.user_dependencies import (
    get_login_user_use_case,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
    use_case: LoginUserUseCase = Depends(get_login_user_use_case),
) -> TokenResponse:
    try:
        access_token = use_case.execute(
            email=request.email,
            password=request.password,
        )

        return TokenResponse(
            access_token=access_token,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc