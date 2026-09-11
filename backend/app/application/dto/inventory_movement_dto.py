from datetime import datetime

from pydantic import BaseModel, Field

from app.domain.entities.movement_type import MovementType


class CreateInventoryMovementRequest(BaseModel):
    product_code: str = Field(..., min_length=2, max_length=50)
    movement_type: MovementType
    quantity: int = Field(..., ge=0)
    reason: str | None = Field(default=None, max_length=255)


class InventoryMovementResponse(BaseModel):
    id: int | None
    product_id: int
    movement_type: MovementType
    quantity: int
    reason: str | None
    sale_id: int | None
    created_at: datetime | None