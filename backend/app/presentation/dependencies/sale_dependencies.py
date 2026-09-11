from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.use_cases.create_sale import CreateSaleUseCase
from app.infrastructure.repositories.postgres_sale_repository import (
    PostgresSaleRepository,
)
from app.presentation.dependencies.database_dependencies import (
    get_db_session,
)
from app.presentation.dependencies.product_dependencies import (
    get_product_repository,
)
from app.application.use_cases.get_sale_by_id import GetSaleByIdUseCase
from app.application.use_cases.list_sales import ListSalesUseCase
from app.presentation.dependencies.inventory_movement_dependencies import (
    get_inventory_movement_repository,
)
from app.application.use_cases.cancel_sale import CancelSaleUseCase


def get_sale_repository(
    db_session: Session = Depends(get_db_session),
) -> PostgresSaleRepository:
    return PostgresSaleRepository(db_session)


def get_create_sale_use_case(
    sale_repository: PostgresSaleRepository = Depends(
        get_sale_repository
    ),
    product_repository=Depends(get_product_repository),
    inventory_movement_repository=Depends(
        get_inventory_movement_repository
    ),
) -> CreateSaleUseCase:
    return CreateSaleUseCase(
        sale_repository=sale_repository,
        product_repository=product_repository,
        inventory_movement_repository=inventory_movement_repository,
    )
    
def get_sale_by_id_use_case(
    sale_repository: PostgresSaleRepository = Depends(
        get_sale_repository
    ),
) -> GetSaleByIdUseCase:
    return GetSaleByIdUseCase(sale_repository)

def get_list_sales_use_case(
    sale_repository: PostgresSaleRepository = Depends(
        get_sale_repository
    ),
) -> ListSalesUseCase:
    return ListSalesUseCase(sale_repository)

def get_cancel_sale_use_case(
    sale_repository: PostgresSaleRepository = Depends(
        get_sale_repository
    ),
    product_repository=Depends(get_product_repository),
    inventory_movement_repository=Depends(
        get_inventory_movement_repository
    ),
) -> CancelSaleUseCase:
    return CancelSaleUseCase(
        sale_repository=sale_repository,
        product_repository=product_repository,
        inventory_movement_repository=inventory_movement_repository,
    )