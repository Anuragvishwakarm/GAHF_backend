from slugify import slugify

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
)


class CategoryService:

    @staticmethod
    async def create(
        data: CategoryCreate,
        db: AsyncSession,
    ):
        result = await db.execute(
            select(Category).where(
                Category.name == data.name
            )
        )

        category = result.scalar_one_or_none()

        if category:
            raise ValueError(
                "Category already exists"
            )

        category = Category(
            name=data.name,
            slug=slugify(data.name),
            description=data.description,
        )

        db.add(category)

        await db.commit()
        await db.refresh(category)

        return category

    @staticmethod
    async def get_all(
        db: AsyncSession,
    ):
        result = await db.execute(
            select(Category)
        )

        return result.scalars().all()

    @staticmethod
    async def get_by_id(
        category_id: str,
        db: AsyncSession,
    ):
        result = await db.execute(
            select(Category).where(
                Category.id == category_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def update(
        category_id: str,
        data: CategoryUpdate,
        db: AsyncSession,
    ):
        result = await db.execute(
            select(Category).where(
                Category.id == category_id
            )
        )

        category = result.scalar_one_or_none()

        if not category:
            return None

        category.name = data.name
        category.slug = slugify(data.name)
        category.description = data.description

        await db.commit()
        await db.refresh(category)

        return category

    @staticmethod
    async def delete(
        category_id: str,
        db: AsyncSession,
    ):
        result = await db.execute(
            select(Category).where(
                Category.id == category_id
            )
        )

        category = result.scalar_one_or_none()

        if not category:
            return False

        await db.delete(category)

        await db.commit()

        return True