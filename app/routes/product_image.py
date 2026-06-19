from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import os
import uuid

from app.core.database import get_db
from app.services.product_image_service import (
    add_product_image,
    get_product_images,
    delete_image,
)

router = APIRouter(prefix="/products", tags=["Product Images"])

UPLOAD_DIR = "uploads"


@router.post("/{product_id}/images")
async def upload_image(
    product_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):

    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Only image files allowed"
        )

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    image_url = f"/uploads/{filename}"

    image = await add_product_image(
        db,
        product_id,
        image_url
    )

    return {
        "message": "Image uploaded successfully",
        "image": image,
    }


@router.get("/{product_id}/images")
async def get_images(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await get_product_images(db, product_id)


@router.delete("/images/{image_id}")
async def remove_image(
    image_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await delete_image(db, image_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Image not found"
        )

    return {"message": "Image deleted"}