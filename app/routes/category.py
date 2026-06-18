from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
)

from app.services.category_service import (
    CategoryService,
)

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.post("/")
async def create_category(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await CategoryService.create(
            data,
            db,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/")
async def get_categories(
    db: AsyncSession = Depends(get_db),
):
    return await CategoryService.get_all(db)


@router.get("/{category_id}")
async def get_category(
    category_id: str,
    db: AsyncSession = Depends(get_db),
):
    category = await CategoryService.get_by_id(
        category_id,
        db,
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    return category


@router.put("/{category_id}")
async def update_category(
    category_id: str,
    data: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
):
    category = await CategoryService.update(
        category_id,
        data,
        db,
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    return category


@router.delete("/{category_id}")
async def delete_category(
    category_id: str,
    db: AsyncSession = Depends(get_db),
):
    deleted = await CategoryService.delete(
        category_id,
        db,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    return {
        "message": "Category deleted"
    }