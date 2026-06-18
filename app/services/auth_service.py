import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime, timedelta
from sqlalchemy import select

from app.models.refresh_token import RefreshToken

from app.models.user import User
from app.schemas.auth import RegisterRequest
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)


class AuthService:

    @staticmethod
    async def register(
        data: RegisterRequest,
        db: AsyncSession,
    ):
        result = await db.execute(
            select(User).where(
                User.email == data.email
            )
        )

        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise ValueError("Email already exists")

        user = User(
            full_name=data.full_name,
            email=data.email,
            password_hash=hash_password(
                data.password
            ),
        )

        db.add(user)

        await db.commit()

        await db.refresh(user)

        return user

    @staticmethod
    async def login(
        email: str,
        password: str,
        db: AsyncSession,
    ):
        result = await db.execute(
            select(User).where(
                User.email == email
            )
        )

        user = result.scalar_one_or_none()

        if not user:
            return None

        if not verify_password(
            password,
            user.password_hash,
        ):
            return None

        access_token = create_access_token(
            {
                "sub": user.email,
                "role": user.role,
            }
        )

        refresh_token = str(uuid.uuid4())

        db_token = RefreshToken(
            user_id=user.id,
            token=refresh_token,
            expires_at=datetime.utcnow() + timedelta(days=30),
        )

        db.add(db_token)

        await db.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    

    @staticmethod
    async def refresh_access_token(
        refresh_token: str,
        db: AsyncSession,
    ):
        result = await db.execute(
            select(RefreshToken).where(
                RefreshToken.token == refresh_token
            )
        )

        token_record = result.scalar_one_or_none()

        if not token_record:
            return None

        if token_record.expires_at < datetime.utcnow():
            return None

        result = await db.execute(
            select(User).where(
                User.id == token_record.user_id
            )
        )

        user = result.scalar_one_or_none()

        if not user:
            return None

        access_token = create_access_token(
            {
                "sub": user.email,
                "role": user.role,
            }
        )

        return access_token


    @staticmethod
    async def logout(
        refresh_token: str,
        db: AsyncSession,
    ):
        result = await db.execute(
            select(RefreshToken).where(
                RefreshToken.token == refresh_token
            )
        )

        token_record = result.scalar_one_or_none()

        if not token_record:
            return False

        await db.delete(token_record)

        await db.commit()

        return True