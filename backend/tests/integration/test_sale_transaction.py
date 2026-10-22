import pytest

from app.domain.entities.audit_action import AuditAction
from app.domain.entities.audit_result import AuditResult
from app.infrastructure.database.models.audit_log_model import (
    AuditLogModel,
)

import app.infrastructure.database.models

from app.application.dto.sale_dto import CreateSaleItemRequest
from app.application.use_cases.create_sale import CreateSaleUseCase

from app.domain.entities.category import Category
from app.domain.entities.product import Product
from app.domain.entities.user import User
from app.domain.entities.user_role import UserRole

from app.infrastructure.repositories.postgres_category_repository import (
    PostgresCategoryRepository,
)
from app.infrastructure.repositories.postgres_product_repository import (
    PostgresProductRepository,
)
from app.infrastructure.repositories.postgres_user_repository import (
    PostgresUserRepository,
)
from app.infrastructure.repositories.postgres_sale_repository import (
    PostgresSaleRepository,
)
from app.infrastructure.repositories.postgres_inventory_movement_repository import (
    PostgresInventoryMovementRepository,
)
from app.infrastructure.unit_of_work import SqlAlchemyUnitOfWork

from app.application.use_cases.cancel_sale import CancelSaleUseCase
from app.domain.entities.sale_status import SaleStatus
from app.infrastructure.repositories.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)

class FailingInventoryMovementRepository(
    PostgresInventoryMovementRepository
):
    def create_without_commit(self, movement):
        raise RuntimeError("Simulated sale transaction failure")

class FailingAuditLogRepository(
    PostgresAuditLogRepository
):
    def create_without_commit(self, audit_log):
        raise RuntimeError("Simulated sale audit failure")

def test_sale_rollback_when_audit_creation_fails(
    db_session,
    seller,
    sale_product,
):
    # Arrange
    product_repository = PostgresProductRepository(
        db_session
    )
    sale_repository = PostgresSaleRepository(
        db_session
    )
    movement_repository = PostgresInventoryMovementRepository(
        db_session
    )
    audit_log_repository = FailingAuditLogRepository(
        db_session
    )
    unit_of_work = SqlAlchemyUnitOfWork(db_session)

    use_case = CreateSaleUseCase(
        sale_repository=sale_repository,
        product_repository=product_repository,
        inventory_movement_repository=movement_repository,
        audit_log_repository=audit_log_repository,
        unit_of_work=unit_of_work,
    )

    # Act
    with pytest.raises(
        RuntimeError,
        match="Simulated sale audit failure",
    ):
        use_case.execute(
            seller_id=seller.id,
            items=[
                CreateSaleItemRequest(
                    product_code=sale_product.code,
                    quantity=3,
                )
            ],
        )

    # Reload database state after rollback
    db_session.expire_all()

    saved_product = product_repository.get_by_code(
        sale_product.code
    )
    saved_sales = sale_repository.list_all()
    saved_movements = movement_repository.list_by_product(
        sale_product.id
    )
    saved_audit_logs = db_session.query(
        AuditLogModel
    ).filter(
        AuditLogModel.action == "SALE_CREATE",
        AuditLogModel.user_id == seller.id,
    ).all()

    # Assert
    assert saved_product is not None
    assert saved_product.current_stock == 10

    assert saved_sales == []
    assert saved_movements == []
    assert saved_audit_logs == []

@pytest.fixture
def seller(db_session):
    user_repository = PostgresUserRepository(db_session)

    user = User(
        id=None,
        name="Integration Test Seller",
        email="seller.sale.integration@test.com",
        hashed_password="test_password_hash",
        role=UserRole.SELLER,
    )

    return user_repository.create(user)

@pytest.fixture
def sale_product(db_session):
    category_repository = PostgresCategoryRepository(db_session)
    product_repository = PostgresProductRepository(db_session)

    category = category_repository.create(
        Category(
            id=None,
            name="Sale Transaction Category",
            description="Category for sale integration testing",
        )
    )

    product = product_repository.create(
        Product(
            id=None,
            name="Gaming Keyboard",
            code="INT-SALE-001",
            description="Product for sale transaction testing",
            price=250000,
            current_stock=10,
            minimum_stock=2,
            category_id=category.id,
        )
    )

    return product

def test_sale_rollback_when_movement_creation_fails(
    db_session,
    seller,
    sale_product,
):
    # Arrange
    product_repository = PostgresProductRepository(db_session)
    sale_repository = PostgresSaleRepository(db_session)

    movement_repository = FailingInventoryMovementRepository(
        db_session
    )
    
    audit_log_repository = PostgresAuditLogRepository(
            db_session
        )

    unit_of_work = SqlAlchemyUnitOfWork(db_session)
    
    use_case = CreateSaleUseCase(
        sale_repository=sale_repository,
        product_repository=product_repository,
        inventory_movement_repository=movement_repository,
        audit_log_repository=audit_log_repository,
        unit_of_work=unit_of_work,
    )

    # Act
    with pytest.raises(
        RuntimeError,
        match="Simulated sale transaction failure",
    ):
        use_case.execute(
            seller_id=seller.id,
            items=[
                CreateSaleItemRequest(
                    product_code=sale_product.code,
                    quantity=3,
                )
            ],
        )

    # Assert: product stock must remain unchanged
    db_session.expire_all()

    saved_product = product_repository.get_by_code(
        sale_product.code
    )

    assert saved_product is not None
    assert saved_product.current_stock == 10

    # Assert: no sale should remain in the database
    saved_sales = sale_repository.list_all()

    assert saved_sales == []

def test_sale_transaction_commits_successfully(
    db_session,
    seller,
    sale_product,
):
    # Arrange
    product_repository = PostgresProductRepository(db_session)
    sale_repository = PostgresSaleRepository(db_session)

    movement_repository = PostgresInventoryMovementRepository(
        db_session
    )
    
    audit_log_repository = PostgresAuditLogRepository(
        db_session
    )

    unit_of_work = SqlAlchemyUnitOfWork(db_session)

    use_case = CreateSaleUseCase(
        sale_repository=sale_repository,
        product_repository=product_repository,
        inventory_movement_repository=movement_repository,
        audit_log_repository=audit_log_repository,
        unit_of_work=unit_of_work,
    )

    # Act
    sale = use_case.execute(
        seller_id=seller.id,
        items=[
            CreateSaleItemRequest(
                product_code=sale_product.code,
                quantity=3,
            )
        ],
    )

    # Assert
    db_session.expire_all()

    saved_product = product_repository.get_by_code(
        sale_product.code
    )

    saved_sale = sale_repository.get_by_id(sale.id)

    movements = movement_repository.list_by_product(
        sale_product.id
    ) 
    
    audit_logs = db_session.query(
        AuditLogModel
    ).filter(
        AuditLogModel.entity_type == "sale",
        AuditLogModel.entity_id == str(sale.id),
    ).all()

    assert saved_product is not None
    assert saved_product.current_stock == 7

    assert saved_sale is not None
    assert saved_sale.seller_id == seller.id

    assert len(movements) == 1
    assert movements[0].quantity == 3
    assert movements[0].sale_id == sale.id
    
    assert len(audit_logs) == 1

    audit_log = audit_logs[0]

    assert audit_log.user_id == seller.id
    assert audit_log.action == AuditAction.SALE_CREATE.value
    assert audit_log.entity_type == "sale"
    assert audit_log.entity_id == str(sale.id)
    assert audit_log.old_values is None
    assert audit_log.result == AuditResult.SUCCESS.value

    assert audit_log.new_values == {
        "seller_id": seller.id,
        "status": sale.status.value,
        "items": [
            {
                "product_id": sale_product.id,
                "quantity": 3,
                "unit_price": str(sale.items[0].unit_price),
            }
        ],
    }

def test_cancel_sale_rollback_when_movement_creation_fails(
    db_session,
    seller,
    sale_product,
):
    product_repository = PostgresProductRepository(db_session)
    sale_repository = PostgresSaleRepository(db_session)
    movement_repository = PostgresInventoryMovementRepository(
        db_session
    )
    
    audit_log_repository = PostgresAuditLogRepository(
        db_session
    )
    
    unit_of_work = SqlAlchemyUnitOfWork(db_session)
    
    # Create a valid sale first
    create_sale_use_case = CreateSaleUseCase(
        sale_repository=sale_repository,
        product_repository=product_repository,
        inventory_movement_repository=movement_repository,
        audit_log_repository=audit_log_repository,
        unit_of_work=unit_of_work,
    )

    sale = create_sale_use_case.execute(
        seller_id=seller.id,
        items=[
            CreateSaleItemRequest(
                product_code=sale_product.code,
                quantity=3,
            )
        ],
    )

    # Simulate a failure during cancellation
    failing_movement_repository = (
        FailingInventoryMovementRepository(db_session)
    )

    cancel_sale_use_case = CancelSaleUseCase(
        sale_repository=sale_repository,
        product_repository=product_repository,
        inventory_movement_repository=failing_movement_repository,
        audit_log_repository=audit_log_repository,
        unit_of_work=unit_of_work,
    )

    with pytest.raises(
        RuntimeError,
        match="Simulated sale transaction failure",
    ):
        cancel_sale_use_case.execute(
            sale_id=sale.id,
            cancelled_by_user_id=seller.id,
        )

    # Reload persisted data after rollback
    db_session.expire_all()

    saved_product = product_repository.get_by_code(
        sale_product.code
    )
    saved_sale = sale_repository.get_by_id(sale.id)
    movements = movement_repository.list_by_product(
        sale_product.id
    )

    assert saved_product is not None
    assert saved_product.current_stock == 7

    assert saved_sale is not None
    assert saved_sale.status != SaleStatus.CANCELLED

    # Only the original sale movement should exist
    assert len(movements) == 1

def test_cancel_sale_transaction_commits_successfully(
    db_session,
    seller,
    sale_product,
):
    # Arrange
    product_repository = PostgresProductRepository(db_session)
    sale_repository = PostgresSaleRepository(db_session)
    movement_repository = PostgresInventoryMovementRepository(
        db_session
    )
    audit_log_repository = PostgresAuditLogRepository(
        db_session
    )
    unit_of_work = SqlAlchemyUnitOfWork(db_session)

    create_sale_use_case = CreateSaleUseCase(
        sale_repository=sale_repository,
        product_repository=product_repository,
        inventory_movement_repository=movement_repository,
        audit_log_repository=audit_log_repository,
        unit_of_work=unit_of_work,
    )

    sale = create_sale_use_case.execute(
        seller_id=seller.id,
        items=[
            CreateSaleItemRequest(
                product_code=sale_product.code,
                quantity=3,
            )
        ],
    )

    cancel_sale_use_case = CancelSaleUseCase(
        sale_repository=sale_repository,
        product_repository=product_repository,
        inventory_movement_repository=movement_repository,
        audit_log_repository=audit_log_repository,
        unit_of_work=unit_of_work,
    )

    # Act
    cancelled_sale = cancel_sale_use_case.execute(
        sale_id=sale.id,
        cancelled_by_user_id=seller.id,
    )

    # Assert
    db_session.expire_all()

    saved_product = product_repository.get_by_code(
        sale_product.code
    )
    saved_sale = sale_repository.get_by_id(sale.id)
    movements = movement_repository.list_by_product(
        sale_product.id
    )

    audit_logs = db_session.query(AuditLogModel).filter(
        AuditLogModel.entity_type == "sale",
        AuditLogModel.entity_id == str(sale.id),
    ).all()

    assert saved_product is not None
    assert saved_product.current_stock == 10

    assert saved_sale is not None
    assert saved_sale.status == SaleStatus.CANCELLED
    assert cancelled_sale.status == SaleStatus.CANCELLED

    assert len(movements) == 2
    assert {movement.movement_type.value for movement in movements} == {
        "entry",
        "exit",
    }

    assert len(audit_logs) == 2

    cancellation_audit = next(
        audit_log
        for audit_log in audit_logs
        if audit_log.action == AuditAction.SALE_CANCEL.value
    )

    assert cancellation_audit.user_id == seller.id
    assert cancellation_audit.entity_type == "sale"
    assert cancellation_audit.entity_id == str(sale.id)
    assert cancellation_audit.result == AuditResult.SUCCESS.value

    assert cancellation_audit.old_values == {
        "status": SaleStatus.COMPLETED.value,
    }

    assert cancellation_audit.new_values == {
        "status": SaleStatus.CANCELLED.value,
        "cancelled_by_user_id": seller.id,
    }

def test_cancel_sale_rollback_when_audit_creation_fails(
    db_session,
    seller,
    sale_product,
):
    # Arrange
    product_repository = PostgresProductRepository(db_session)
    sale_repository = PostgresSaleRepository(db_session)
    movement_repository = PostgresInventoryMovementRepository(
        db_session
    )
    audit_log_repository = PostgresAuditLogRepository(
        db_session
    )
    unit_of_work = SqlAlchemyUnitOfWork(db_session)

    # Create a valid sale first
    create_sale_use_case = CreateSaleUseCase(
        sale_repository=sale_repository,
        product_repository=product_repository,
        inventory_movement_repository=movement_repository,
        audit_log_repository=audit_log_repository,
        unit_of_work=unit_of_work,
    )

    sale = create_sale_use_case.execute(
        seller_id=seller.id,
        items=[
            CreateSaleItemRequest(
                product_code=sale_product.code,
                quantity=3,
            )
        ],
    )

    # Simulate an audit failure during cancellation
    failing_audit_repository = FailingAuditLogRepository(
        db_session
    )

    cancel_sale_use_case = CancelSaleUseCase(
        sale_repository=sale_repository,
        product_repository=product_repository,
        inventory_movement_repository=movement_repository,
        audit_log_repository=failing_audit_repository,
        unit_of_work=unit_of_work,
    )

    # Act
    with pytest.raises(
        RuntimeError,
        match="Simulated sale audit failure",
    ):
        cancel_sale_use_case.execute(
            sale_id=sale.id,
            cancelled_by_user_id=seller.id,
        )

    # Reload persisted state after rollback
    db_session.expire_all()

    saved_product = product_repository.get_by_code(
        sale_product.code
    )
    saved_sale = sale_repository.get_by_id(sale.id)
    movements = movement_repository.list_by_product(
        sale_product.id
    )

    audit_logs = db_session.query(AuditLogModel).filter(
        AuditLogModel.entity_type == "sale",
        AuditLogModel.entity_id == str(sale.id),
    ).all()

    # Assert
    assert saved_product is not None
    assert saved_product.current_stock == 7

    assert saved_sale is not None
    assert saved_sale.status == SaleStatus.COMPLETED

    assert len(movements) == 1
    assert movements[0].movement_type.value == "exit"
    assert movements[0].quantity == 3

    assert len(audit_logs) == 1
    assert audit_logs[0].action == AuditAction.SALE_CREATE.value
