from fastapi import Depends

from app.application.use_cases.get_dashboard_summary import (
    GetDashboardSummaryUseCase,
)
from app.infrastructure.repositories.postgres_product_repository import (
    PostgresProductRepository,
)
from app.infrastructure.repositories.postgres_sale_repository import (
    PostgresSaleRepository,
)
from app.presentation.dependencies.product_dependencies import (
    get_product_repository,
)
from app.presentation.dependencies.sale_dependencies import (
    get_sale_repository,
)


def get_dashboard_summary_use_case(
    product_repository: PostgresProductRepository = Depends(
        get_product_repository
    ),
    sale_repository: PostgresSaleRepository = Depends(
        get_sale_repository
    ),
) -> GetDashboardSummaryUseCase:
    return GetDashboardSummaryUseCase(
        product_repository=product_repository,
        sale_repository=sale_repository,
    )