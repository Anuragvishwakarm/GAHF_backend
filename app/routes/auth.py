from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    RefreshTokenRequest,
)

from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register")
async def register(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        user = await AuthService.register(
            data,
            db,
        )

        return {
            "message": "User registered",
            "user_id": user.id,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post("/login")
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    tokens = await AuthService.login(
        data.email,
        data.password,
        db,
    )

    if not tokens:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    return tokens


@router.post("/refresh")
async def refresh_token(
    data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    token = await AuthService.refresh_access_token(
        data.refresh_token,
        db,
    )

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token",
        )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.post("/logout")
async def logout(
    data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    success = await AuthService.logout(
        data.refresh_token,
        db,
    )

    if not success:
        raise HTTPException(
            status_code=400,
            detail="Invalid refresh token",
        )

    return {
        "message": "Logged out successfully",
    }