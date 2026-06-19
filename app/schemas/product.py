from pydantic import BaseModel
from typing import Optional, List


class ProductImageOut(BaseModel):
    id: int
    image_url: str
    is_primary: bool

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category_id: int


class ProductCreate(ProductBase):
    name: str
    description: str | None = None
    price: float
    category_id: int
    stock: int


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None


class ProductOut(ProductBase):
    id: int
    stock: int
    images: List[ProductImageOut] = []

    class Config:
        from_attributes = True