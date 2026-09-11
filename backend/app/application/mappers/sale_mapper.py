from app.application.dto.sale_dto import (
    SaleItemResponse,
    SaleResponse,
)
from app.domain.entities.sale import Sale


class SaleMapper:
    @staticmethod
    def entity_to_response(
        sale: Sale,
    ) -> SaleResponse:
        return SaleResponse(
            id=sale.id,
            seller_id=sale.seller_id,
            status=sale.status,
            total=sale.total,
            created_at=sale.created_at,
            items=[
                SaleItemResponse(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    subtotal=item.subtotal,
                )
                for item in sale.items
            ],
        )