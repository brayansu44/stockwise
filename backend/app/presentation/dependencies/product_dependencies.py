from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.use_cases.create_product import CreateProductUseCase
from app.application.use_cases.get_product_by_code import GetProductByCodeUseCase
from app.application.use_cases.list_products import ListProductsUseCase
from app.infrastructure.repositories.postgres_product_repository import (
    PostgresProductRepository,
)
from app.presentation.dependencies.database_dependencies import get_db_session
from app.application.use_cases.update_product import UpdateProductUseCase
from app.application.use_cases.change_product_status import (
    ChangeProductStatusUseCase,
)
from app.application.use_cases.list_low_stock_products import (
    ListLowStockProductsUseCase,
)

def get_product_repository(
    db_session: Session = Depends(get_db_session),
) -> PostgresProductRepository:
    return PostgresProductRepository(db_session)


def get_create_product_use_case(
    product_repository: PostgresProductRepository = Depends(get_product_repository),
) -> CreateProductUseCase:
    return CreateProductUseCase(product_repository)


def get_list_products_use_case(
    product_repository: PostgresProductRepository = Depends(get_product_repository),
) -> ListProductsUseCase:
    return ListProductsUseCase(product_repository)


def get_product_by_code_use_case(
    product_repository: PostgresProductRepository = Depends(get_product_repository),
) -> GetProductByCodeUseCase:
    return GetProductByCodeUseCase(product_repository)

def get_update_product_use_case(
    product_repository: PostgresProductRepository = Depends(get_product_repository),
) -> UpdateProductUseCase:
    return UpdateProductUseCase(product_repository)

def get_change_product_status_use_case(
    product_repository: PostgresProductRepository = Depends(get_product_repository),
) -> ChangeProductStatusUseCase:
    return ChangeProductStatusUseCase(product_repository)

def get_list_low_stock_products_use_case(
    product_repository: PostgresProductRepository = Depends(
        get_product_repository
    ),
) -> ListLowStockProductsUseCase:
    return ListLowStockProductsUseCase(
        product_repository=product_repository,
    )