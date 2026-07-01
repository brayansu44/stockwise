from pydantic import BaseModel, Field


class CreateProductRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    code: str = Field(..., min_length=2, max_length=50)
    description: str | None = None
    price: float = Field(..., ge=0)
    current_stock: int = Field(..., ge=0)
    minimum_stock: int = Field(..., ge=0)


class ProductResponse(BaseModel):
    id: int | None
    name: str
    code: str
    description: str | None
    price: float
    current_stock: int
    minimum_stock: int
    is_active: bool