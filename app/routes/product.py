from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut
from app.services import product_service

router = APIRouter(prefix="/products", tags=["Products"])


# CREATE PRODUCT
@router.post("/", response_model=ProductOut)
async def create_product(
    data: ProductCreate,
    db: AsyncSession = Depends(get_db)
):
    return await product_service.create_product(db, data)


# GET ALL PRODUCTS
@router.get("/", response_model=list[ProductOut])
async def get_products(db: AsyncSession = Depends(get_db)):
    return await product_service.get_products(db)


# GET SINGLE PRODUCT
@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await product_service.get_product(db, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


# UPDATE PRODUCT
@router.put("/{product_id}", response_model=ProductOut)
async def update_product(
    product_id: int,
    data: ProductUpdate,
    db: AsyncSession = Depends(get_db)
):
    product = await product_service.update_product(db, product_id, data)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


# DELETE PRODUCT
@router.delete("/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await product_service.delete_product(db, product_id)

    if not result:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product deleted successfully"}