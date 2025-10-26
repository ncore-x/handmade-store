from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.base import BaseRepository
from src.models.admin import AdminsOrm


class AdminRepository(BaseRepository[AdminsOrm]):
    def __init__(self):
        super().__init__(AdminsOrm)

    async def get_by_username(self, db: AsyncSession, username: str) -> Optional[AdminsOrm]:
        """Найти администратора по имени пользователя"""
        result = await db.execute(
            select(AdminsOrm).where(AdminsOrm.username == username)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[AdminsOrm]:
        """Найти администратора по email"""
        result = await db.execute(
            select(AdminsOrm).where(AdminsOrm.email == email)
        )
        return result.scalar_one_or_none()

    async def update_last_login(self, db: AsyncSession, admin_id: int) -> None:
        """Обновить время последнего входа"""
        from sqlalchemy import update
        from datetime import datetime

        await db.execute(
            update(AdminsOrm)
            .where(AdminsOrm.id == admin_id)
            .values(last_login=datetime.utcnow())
        )
        await db.commit()
