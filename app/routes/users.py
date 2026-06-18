from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import UpdateProfileRequest,ChangePasswordRequest
from app.models.user import User
from app.core.dependencies import get_current_user

from app.core.security import (
    verify_password,
    hash_password,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get("/me")
async def get_me(
    current_user:User=Depends(get_current_user),
):
    return{
        "id":current_user.id,
        "full_name":current_user.full_name,
        "email":current_user.email,
        "roll":current_user.role,
    }

@router.put("/me")
async def update_profile(
    data: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    current_user.full_name = data.full_name

    await db.commit()
    await db.refresh(current_user)

    return {
        "message": "Profile updated",
    }

@router.patch("/change-password")
async def change_password(
    data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not verify_password(
        data.current_password,
        current_user.password_hash,
    ):
        return {
            "message": "Current password incorrect"
        }

    current_user.password_hash = hash_password(
        data.new_password
    )

    await db.commit()

    return {
        "message": "Password changed successfully"
    }