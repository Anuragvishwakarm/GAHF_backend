from datetime import datetime
import uuid
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String,Boolean,DateTime

from app.core.database import Base

class User(Base):

    __tablename__="users"
    id:Mapped[str] = mapped_column(String,primary_key=True,default=lambda:str(uuid.uuid4()),)
    full_name: Mapped[str] =  mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255),unique=True,index=True,)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20),default="CUSTOMER",)
    is_active: Mapped[bool] = mapped_column(Boolean,default=True,)
    created_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow)

