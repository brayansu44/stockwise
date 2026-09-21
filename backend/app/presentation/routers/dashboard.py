from fastapi import APIRouter, Depends

from app.application.dto.dashboard_dto import DashboardSummary
from app.application.use_cases.get_dashboard_summary import (
    GetDashboardSummaryUseCase,
)
from app.presentation.dependencies.auth_dependencies import (
    get_current_user,
)
from app.presentation.dependencies.dashboard_dependencies import (
    get_dashboard_summary_use_case,
)
from app.domain.entities.user import User


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/summary",
    response_model=DashboardSummary,
)
def get_dashboard_summary(
    use_case: GetDashboardSummaryUseCase = Depends(
        get_dashboard_summary_use_case
    ),
    current_user: User = Depends(get_current_user),
) -> DashboardSummary:
    return use_case.execute()