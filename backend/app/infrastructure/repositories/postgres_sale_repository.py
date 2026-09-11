from decimal import Decimal

from sqlalchemy.orm import Session

from app.domain.entities.sale import Sale
from app.domain.repositories.sale_repository import SaleRepository
from app.infrastructure.database.models.sale_item_model import SaleItemModel
from app.infrastructure.database.models.sale_model import SaleModel
from app.domain.entities.sale_item import SaleItem
from app.domain.entities.sale_status import SaleStatus

class PostgresSaleRepository(SaleRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, sale: Sale) -> Sale:
        try:
            sale_model = SaleModel(
                seller_id=sale.seller_id,
                status=sale.status.value,
            )

            self.db_session.add(sale_model)
            self.db_session.flush()

            for item in sale.items:
                sale_item_model = SaleItemModel(
                    sale_id=sale_model.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=Decimal(str(item.unit_price)),
                )

                self.db_session.add(sale_item_model)

            self.db_session.commit()
            self.db_session.refresh(sale_model)

            sale.id = sale_model.id
            sale.created_at = sale_model.created_at

            return sale

        except Exception:
            self.db_session.rollback()
            raise
    
    def create_without_commit(
        self,
        sale: Sale,
    ) -> Sale:
        sale_model = SaleModel(
            seller_id=sale.seller_id,
            status=sale.status.value,
        )

        self.db_session.add(sale_model)
        self.db_session.flush()

        for item in sale.items:
            sale_item_model = SaleItemModel(
                sale_id=sale_model.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=Decimal(str(item.unit_price)),
            )

            self.db_session.add(sale_item_model)

        self.db_session.flush()

        sale.id = sale_model.id
        sale.created_at = sale_model.created_at

        return sale
    
    def get_by_id(
        self,
        sale_id: int,
    ) -> Sale | None:
        sale_model = (
            self.db_session.query(SaleModel)
            .filter(SaleModel.id == sale_id)
            .first()
        )

        if not sale_model:
            return None

        item_models = (
            self.db_session.query(SaleItemModel)
            .filter(SaleItemModel.sale_id == sale_model.id)
            .all()
        )

        items = [
            SaleItem(
                product_id=item_model.product_id,
                quantity=item_model.quantity,
                unit_price=float(item_model.unit_price),
            )
            for item_model in item_models
        ]

        return Sale(
            id=sale_model.id,
            seller_id=sale_model.seller_id,
            items=items,
            status=SaleStatus(sale_model.status),
            created_at=sale_model.created_at,
        )
    
    def list_all(self) -> list[Sale]:
        sale_models = (
            self.db_session.query(SaleModel)
            .order_by(SaleModel.created_at.desc())
            .all()
        )

        sales: list[Sale] = []

        for sale_model in sale_models:
            item_models = (
                self.db_session.query(SaleItemModel)
                .filter(SaleItemModel.sale_id == sale_model.id)
                .all()
            )

            items = [
                SaleItem(
                    product_id=item_model.product_id,
                    quantity=item_model.quantity,
                    unit_price=float(item_model.unit_price),
                )
                for item_model in item_models
            ]

            sales.append(
                Sale(
                    id=sale_model.id,
                    seller_id=sale_model.seller_id,
                    items=items,
                    status=SaleStatus(sale_model.status),
                    created_at=sale_model.created_at,
                )
            )

        return sales
    
    def commit(self) -> None:
        try:
            self.db_session.commit()
        except Exception:
            self.db_session.rollback()
            raise
        
    def update_without_commit(
        self,
        sale: Sale,
    ) -> Sale:
        sale_model = (
            self.db_session.query(SaleModel)
            .filter(SaleModel.id == sale.id)
            .first()
        )

        if not sale_model:
            raise ValueError("Sale not found")

        sale_model.status = sale.status.value

        self.db_session.flush()

        return sale