from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    description: str | None = None


class CategoryUpdate(BaseModel):
    name: str
    description: str | None = None


class CategoryResponse(BaseModel):
    id: str
    name: str
    slug: str
    description: str | None
    is_active: bool

    class Config:
        from_attributes = True