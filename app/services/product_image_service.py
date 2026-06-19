from sqlalchemy import select
from app.models.product_image import ProductImage


async def add_product_image(
    db,
    product_id: int,
    image_url: str,
    is_primary: bool = False,
):
    image = ProductImage(
        product_id=product_id,
        image_url=image_url,
        is_primary=is_primary
    )

    db.add(image)

    await db.commit()
    await db.refresh(image)

    return image


async def get_product_images(db, product_id: int):
    result = await db.execute(
        select(ProductImage).where(
            ProductImage.product_id == product_id
        )
    )

    return result.scalars().all()


async def delete_image(db, image_id: int):

    result = await db.execute(
        select(ProductImage).where(
            ProductImage.id == image_id
        )
    )

    image = result.scalar_one_or_none()

    if not image:
        return None

    await db.delete(image)
    await db.commit()

    return True