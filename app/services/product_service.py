from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product


# CREATE PRODUCT
async def create_product(db: AsyncSession, data):
    product = Product(**data.dict())

    db.add(product)
    await db.commit()
    await db.refresh(product)

    return product


# GET ALL PRODUCTS
async def get_products(db: AsyncSession):
    result = await db.execute(select(Product))
    return result.scalars().all()


# GET SINGLE PRODUCT
async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    return result.scalar_one_or_none()


# UPDATE PRODUCT
async def update_product(db: AsyncSession, product_id: int, data):
    product = await get_product(db, product_id)

    if not product:
        return None

    for key, value in data.dict(exclude_unset=True).items():
        setattr(product, key, value)

    await db.commit()
    await db.refresh(product)

    return product


# DELETE PRODUCT
async def delete_product(db: AsyncSession, product_id: int):
    product = await get_product(db, product_id)

    if not product:
        return None

    await db.delete(product)
    await db.commit()

    return True