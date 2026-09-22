from pydantic import BaseModel


class CreateCategoryRequest(BaseModel):
    name: str
    description: str | None = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str | None
    is_active: bool
    
class UpdateCategoryRequest(BaseModel):
    name: str
    description: str | None = None