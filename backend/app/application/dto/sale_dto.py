from datetime import datetime

from pydantic import BaseModel, Field

from app.domain.entities.sale_status import SaleStatus


class CreateSaleItemRequest(BaseModel):
    product_code: str = Field(..., min_length=2, max_length=50)
    quantity: int = Field(..., gt=0)


class CreateSaleRequest(BaseModel):
    items: list[CreateSaleItemRequest] = Field(..., min_length=1)


class SaleItemResponse(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    subtotal: float


class SaleResponse(BaseModel):
    id: int | None
    seller_id: int
    status: SaleStatus
    total: float
    created_at: datetime | None
    items: list[SaleItemResponse]