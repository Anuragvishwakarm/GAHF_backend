from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)

    category_id = Column(Integer, ForeignKey("categories.id"))
    stock = Column(Integer, default=0, nullable=False)
    low_stock_threshold = Column(Integer, default=5,nullable=False)

    images = relationship("ProductImage", back_populates="product", cascade="all, delete",lazy="selectin")