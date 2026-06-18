from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import os
import uuid

from app.core.database import get_db
from app.services.product_image_service import add_product_image, get_product_images, delete_image

router = APIRouter(prefix="/products", tags=["Product Images"])

UPLOAD_DIR = "uploads"


# 📌 UPLOAD IMAGE
@router.post("/{product_id}/images")
async def upload_image(
    product_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # 1. validate file
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files allowed")

    # 2. generate unique filename
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    # 3. save file
    with open(file_path, "wb") as f:
        f.write(await file.read())

    image_url = f"/uploads/{filename}"

    # 4. save in DB
    image = add_product_image(db, product_id, image_url)

    return {
        "message": "Image uploaded successfully",
        "image": image
    }


# 📌 GET ALL IMAGES OF PRODUCT
@router.get("/{product_id}/images")
def get_images(product_id: int, db: Session = Depends(get_db)):
    return get_product_images(db, product_id)


# 📌 DELETE IMAGE
@router.delete("/images/{image_id}")
def remove_image(image_id: int, db: Session = Depends(get_db)):
    result = delete_image(db, image_id)

    if not result:
        raise HTTPException(status_code=404, detail="Image not found")

    return {"message": "Image deleted"}