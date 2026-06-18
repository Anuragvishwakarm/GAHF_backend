from sqlalchemy.orm import Session
from app.models.product_image import ProductImage


def add_product_image(db: Session, product_id: int, image_url: str, is_primary: bool = False):
    image = ProductImage(
        product_id=product_id,
        image_url=image_url,
        is_primary=is_primary
    )

    db.add(image)
    db.commit()
    db.refresh(image)
    return image


def get_product_images(db: Session, product_id: int):
    return db.query(ProductImage).filter(ProductImage.product_id == product_id).all()


def delete_image(db: Session, image_id: int):
    image = db.query(ProductImage).filter(ProductImage.id == image_id).first()

    if not image:
        return None

    db.delete(image)
    db.commit()
    return True