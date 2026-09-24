from fastapi import status

from app.domain.entities.user import User
from app.domain.entities.user_role import UserRole
from app.infrastructure.repositories.postgres_user_repository import (
    PostgresUserRepository,
)
from app.infrastructure.security.jwt_token_service import (
    JwtTokenService,
)

from app.domain.entities.category import Category
from app.domain.entities.product import Product
from app.infrastructure.repositories.postgres_category_repository import (
    PostgresCategoryRepository,
)
from app.infrastructure.repositories.postgres_product_repository import (
    PostgresProductRepository,
)

from app.domain.entities.movement_type import MovementType
from app.infrastructure.repositories.postgres_inventory_movement_repository import (
    PostgresInventoryMovementRepository,
)

from app.domain.entities.sale_status import SaleStatus

from app.domain.entities.sale import Sale
from app.domain.entities.sale_item import SaleItem

from app.infrastructure.repositories.postgres_sale_repository import (
    PostgresSaleRepository,
)

def test_list_sales_without_authentication(client):
    # Act
    response = client.get("/sales/")

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_list_sales_as_admin(client, db_session):
    # Arrange: Create an administrator
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="Sales Test Admin",
            email="sales.admin@test.com",
            hashed_password="test_password_hash",
            role=UserRole.ADMIN,
        )
    )

    token = JwtTokenService().create_access_token(
        subject=str(admin.id)
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Act
    response = client.get(
        "/sales/",
        headers=headers,
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

def test_list_sales_as_inventory_operator_forbidden(
    client,
    db_session,
):
    # Arrange
    user_repository = PostgresUserRepository(db_session)

    operator = user_repository.create(
        User(
            id=None,
            name="Inventory Operator",
            email="sales.operator@test.com",
            hashed_password="test_password_hash",
            role=UserRole.INVENTORY_OPERATOR,
        )
    )

    token = JwtTokenService().create_access_token(
        subject=str(operator.id)
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Act
    response = client.get(
        "/sales/",
        headers=headers,
    )

    # Assert
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_create_sale_as_admin_updates_stock(client, db_session):
    # Arrange: Create an administrator
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="Sales Creation Admin",
            email="sales.creation.admin@test.com",
            hashed_password="test_password_hash",
            role=UserRole.ADMIN,
        )
    )

    token = JwtTokenService().create_access_token(
        subject=str(admin.id)
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Create a category
    category_repository = PostgresCategoryRepository(db_session)

    category = category_repository.create(
        Category(
            id=None,
            name="Sales Test Category",
            description="Category for sales tests",
        )
    )

    # Create a product with 10 units
    product_repository = PostgresProductRepository(db_session)

    product = product_repository.create(
        Product(
            id=None,
            name="Sales Test Product",
            code="SALE-TEST-001",
            description="Product for sales tests",
            price=50.0,
            current_stock=10,
            minimum_stock=2,
            category_id=category.id,
        )
    )

    # Act: Sell 2 units
    response = client.post(
        "/sales/",
        json={
            "items": [
                {
                    "product_code": product.code,
                    "quantity": 2,
                }
            ]
        },
        headers=headers,
    )

    # Assert: Sale was created
    assert response.status_code == status.HTTP_201_CREATED

    sale_data = response.json()

    assert sale_data["id"] is not None
    assert sale_data["seller_id"] == admin.id
        # Assert: Created sale can be retrieved by ID
    get_response = client.get(
        f"/sales/{sale_data['id']}",
        headers=headers,
    )

    assert get_response.status_code == status.HTTP_200_OK

    retrieved_sale = get_response.json()

    assert retrieved_sale["id"] == sale_data["id"]
    assert retrieved_sale["seller_id"] == admin.id
    assert retrieved_sale["total"] == 100.0
    assert len(retrieved_sale["items"]) == 1
    assert sale_data["total"] == 100.0
    assert len(sale_data["items"]) == 1
    assert sale_data["items"][0]["quantity"] == 2

    # Assert: Stock was updated
    db_session.expire_all()

    updated_product = product_repository.get_by_code(product.code)

    assert updated_product is not None
    assert updated_product.current_stock == 8
    
        # Assert: Inventory exit movement was registered
    movement_repository = PostgresInventoryMovementRepository(
        db_session
    )

    movements = movement_repository.list_by_product(
        product.id
    )

    sale_movements = [
        movement
        for movement in movements
        if movement.sale_id == sale_data["id"]
    ]

    assert len(sale_movements) == 1

    movement = sale_movements[0]

    assert movement.product_id == product.id
    assert movement.movement_type == MovementType.EXIT
    assert movement.quantity == 2
    assert movement.reason == f"Sale #{sale_data['id']}"
    
        # Act: Cancel the sale
    cancel_response = client.patch(
        f"/sales/{sale_data['id']}/cancel",
        headers=headers,
    )

    # Assert: Sale was cancelled
    assert cancel_response.status_code == status.HTTP_200_OK

    cancelled_sale = cancel_response.json()

    assert cancelled_sale["id"] == sale_data["id"]
    assert cancelled_sale["status"] == SaleStatus.CANCELLED.value

    # Assert: Original stock was restored
    db_session.expire_all()

    restored_product = product_repository.get_by_code(
        product.code
    )

    assert restored_product is not None
    assert restored_product.current_stock == 10

    # Assert: Inventory entry movement was registered
    movements = movement_repository.list_by_product(
        product.id
    )

    cancellation_movements = [
        movement
        for movement in movements
        if (
            movement.sale_id == sale_data["id"]
            and movement.movement_type == MovementType.ENTRY
        )
    ]

    assert len(cancellation_movements) == 1

    movement = cancellation_movements[0]

    assert movement.quantity == 2
    assert movement.reason == (
        f"Sale cancellation #{sale_data['id']}"
    )
    
        # Act: Attempt to cancel the same sale again
    second_cancel_response = client.patch(
        f"/sales/{sale_data['id']}/cancel",
        headers=headers,
    )

    # Assert: Second cancellation is rejected
    assert second_cancel_response.status_code == (
        status.HTTP_400_BAD_REQUEST
    )

    assert second_cancel_response.json()["detail"] == (
        "Sale is already cancelled"
    )

    # Assert: Stock was not restored twice
    db_session.expire_all()

    product_after_second_attempt = (
        product_repository.get_by_code(product.code)
    )

    assert product_after_second_attempt.current_stock == 10

def test_create_sale_with_insufficient_stock(
    client,
    db_session,
):
    # Arrange: Create an administrator
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="Insufficient Stock Admin",
            email="insufficient.stock@test.com",
            hashed_password="test_password_hash",
            role=UserRole.ADMIN,
        )
    )

    token = JwtTokenService().create_access_token(
        subject=str(admin.id)
    )

    # Create a category
    category_repository = PostgresCategoryRepository(db_session)

    category = category_repository.create(
        Category(
            id=None,
            name="Insufficient Stock Category",
            description="Category for stock validation",
        )
    )

    # Create a product with only 5 units
    product_repository = PostgresProductRepository(db_session)

    product = product_repository.create(
        Product(
            id=None,
            name="Limited Stock Product",
            code="SALE-STOCK-001",
            description="Product with limited stock",
            price=50.0,
            current_stock=5,
            minimum_stock=2,
            category_id=category.id,
        )
    )

    # Act: Attempt to sell 10 units
    response = client.post(
        "/sales/",
        json={
            "items": [
                {
                    "product_code": product.code,
                    "quantity": 10,
                }
            ]
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    # Assert: Sale is rejected
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Insufficient stock"

    # Assert: Stock remains unchanged
    db_session.expire_all()

    updated_product = product_repository.get_by_code(
        product.code
    )

    assert updated_product is not None
    assert updated_product.current_stock == 5

def test_create_sale_with_nonexistent_product(
    client,
    db_session,
):
    # Arrange
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="Nonexistent Product Admin",
            email="nonexistent.product@test.com",
            hashed_password="test_password_hash",
            role=UserRole.ADMIN,
        )
    )

    token = JwtTokenService().create_access_token(
        subject=str(admin.id)
    )

    # Act
    response = client.post(
        "/sales/",
        json={
            "items": [
                {
                    "product_code": "NOT-EXIST-999",
                    "quantity": 2,
                }
            ]
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response.json()["detail"] == (
        "Product not found: NOT-EXIST-999"
    )

def test_create_sale_with_duplicate_products(
    client,
    db_session,
):
    # Arrange: Create an administrator
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="Duplicate Products Admin",
            email="duplicate.products@test.com",
            hashed_password="test_password_hash",
            role=UserRole.ADMIN,
        )
    )

    token = JwtTokenService().create_access_token(
        subject=str(admin.id)
    )

    # Act: Include the same product twice
    response = client.post(
        "/sales/",
        json={
            "items": [
                {
                    "product_code": "DUPLICATE-001",
                    "quantity": 2,
                },
                {
                    "product_code": "DUPLICATE-001",
                    "quantity": 3,
                },
            ]
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response.json()["detail"] == (
        "Duplicate product in sale: DUPLICATE-001"
    )

def test_get_nonexistent_sale_as_admin(
    client,
    db_session,
):
    # Arrange
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="Sales Query Admin",
            email="sales.query.admin@test.com",
            hashed_password="test_password_hash",
            role=UserRole.ADMIN,
        )
    )

    token = JwtTokenService().create_access_token(
        subject=str(admin.id)
    )

    # Act
    response = client.get(
        "/sales/999999",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_cancel_sale_as_seller_forbidden(
    client,
    db_session,
):
    # Arrange: Create a seller
    user_repository = PostgresUserRepository(db_session)

    seller = user_repository.create(
        User(
            id=None,
            name="Sales Cancellation Seller",
            email="sales.cancel.seller@test.com",
            hashed_password="test_password_hash",
            role=UserRole.SELLER,
        )
    )

    token = JwtTokenService().create_access_token(
        subject=str(seller.id)
    )

    # Act: Attempt to cancel a sale
    response = client.patch(
        "/sales/999999/cancel",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    # Assert: Seller does not have permission
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_get_sale_by_id_as_seller(
    client,
    db_session,
):
    # Arrange: Create a seller
    user_repository = PostgresUserRepository(db_session)

    seller = user_repository.create(
        User(
            id=None,
            name="Sales Query Seller",
            email="sales.query.seller@test.com",
            hashed_password="test_password_hash",
            role=UserRole.SELLER,
        )
    )

    token = JwtTokenService().create_access_token(
        subject=str(seller.id)
    )

    # Create a category
    category_repository = PostgresCategoryRepository(db_session)

    category = category_repository.create(
        Category(
            id=None,
            name="Seller Sales Category",
            description="Category for seller sales test",
        )
    )

    # Create a product
    product_repository = PostgresProductRepository(db_session)

    product = product_repository.create(
        Product(
            id=None,
            name="Seller Sales Product",
            code="SELLER-SALE-001",
            description="Product for seller sales test",
            price=100.0,
            current_stock=10,
            minimum_stock=2,
            category_id=category.id,
        )
    )

    # Create the sale directly
    sale_repository = PostgresSaleRepository(db_session)

    sale = Sale(
        id=None,
        seller_id=seller.id,
        items=[
            SaleItem(
                product_id=product.id,
                quantity=2,
                unit_price=product.price,
            )
        ],
    )

    created_sale = sale_repository.create(sale)

    # Act
    response = client.get(
        f"/sales/{created_sale.id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK

    sale_data = response.json()

    assert sale_data["id"] == created_sale.id
    assert sale_data["seller_id"] == seller.id
    assert sale_data["total"] == 200.0
    assert len(sale_data["items"]) == 1
    assert sale_data["items"][0]["quantity"] == 2

def test_list_sales_as_seller(
    client,
    db_session,
):
    # Arrange: Create a seller
    user_repository = PostgresUserRepository(db_session)

    seller = user_repository.create(
        User(
            id=None,
            name="Sales List Seller",
            email="sales.list.seller@test.com",
            hashed_password="test_password_hash",
            role=UserRole.SELLER,
        )
    )

    token = JwtTokenService().create_access_token(
        subject=str(seller.id)
    )

    # Create a category
    category_repository = PostgresCategoryRepository(db_session)

    category = category_repository.create(
        Category(
            id=None,
            name="Sales List Category",
            description="Category for sales list test",
        )
    )

    # Create a product
    product_repository = PostgresProductRepository(db_session)

    product = product_repository.create(
        Product(
            id=None,
            name="Sales List Product",
            code="SALES-LIST-001",
            description="Product for sales list test",
            price=75.0,
            current_stock=10,
            minimum_stock=2,
            category_id=category.id,
        )
    )

    # Create a sale directly
    sale_repository = PostgresSaleRepository(db_session)

    sale = Sale(
        id=None,
        seller_id=seller.id,
        items=[
            SaleItem(
                product_id=product.id,
                quantity=2,
                unit_price=product.price,
            )
        ],
    )

    created_sale = sale_repository.create(sale)

    # Act
    response = client.get(
        "/sales/",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK

    sales_data = response.json()

    assert isinstance(sales_data, list)

    matching_sales = [
        sale_data
        for sale_data in sales_data
        if sale_data["id"] == created_sale.id
    ]

    assert len(matching_sales) == 1

    listed_sale = matching_sales[0]

    assert listed_sale["seller_id"] == seller.id
    assert listed_sale["total"] == 150.0
    assert len(listed_sale["items"]) == 1

def test_create_sale_as_inventory_operator_forbidden(
    client,
    db_session,
):
    # Arrange: Create an inventory operator
    user_repository = PostgresUserRepository(db_session)

    operator = user_repository.create(
        User(
            id=None,
            name="Inventory Operator",
            email="sales.operator@test.com",
            hashed_password="test_password_hash",
            role=UserRole.INVENTORY_OPERATOR,
        )
    )

    token = JwtTokenService().create_access_token(
        subject=str(operator.id)
    )

    # Act
    response = client.post(
        "/sales/",
        json={
            "items": [
                {
                    "product_code": "ANY-PRODUCT",
                    "quantity": 1,
                }
            ]
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    # Assert
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_cancel_sale_as_seller_forbidden_on_existing_sale(
    client,
    db_session,
):
    # Arrange: Create an admin
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="Sale Owner Admin",
            email="sale.owner.admin@test.com",
            hashed_password="test_password_hash",
            role=UserRole.ADMIN,
        )
    )

    # Create a seller
    seller = user_repository.create(
        User(
            id=None,
            name="Sale Cancellation Seller",
            email="sale.existing.cancel.seller@test.com",
            hashed_password="test_password_hash",
            role=UserRole.SELLER,
        )
    )

    # Create a category
    category_repository = PostgresCategoryRepository(db_session)

    category = category_repository.create(
        Category(
            id=None,
            name="Existing Sale Category",
            description="Category for cancellation permission test",
        )
    )

    # Create a product
    product_repository = PostgresProductRepository(db_session)

    product = product_repository.create(
        Product(
            id=None,
            name="Existing Sale Product",
            code="EXISTING-SALE-001",
            description="Product for cancellation permission test",
            price=100.0,
            current_stock=10,
            minimum_stock=2,
            category_id=category.id,
        )
    )

    # Create an existing sale
    sale_repository = PostgresSaleRepository(db_session)

    sale = Sale(
        id=None,
        seller_id=admin.id,
        items=[
            SaleItem(
                product_id=product.id,
                quantity=1,
                unit_price=product.price,
            )
        ],
    )

    created_sale = sale_repository.create(sale)

    # Authenticate as seller
    token = JwtTokenService().create_access_token(
        subject=str(seller.id)
    )

    # Act
    response = client.patch(
        f"/sales/{created_sale.id}/cancel",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    # Assert: Seller is forbidden
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Assert: Sale remains unchanged
    db_session.expire_all()

    persisted_sale = sale_repository.get_by_id(
        created_sale.id
    )

    assert persisted_sale is not None
    assert persisted_sale.status == SaleStatus.COMPLETED
