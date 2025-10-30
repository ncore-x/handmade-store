from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.admin import AdminWithHashedPassword
from src.repositories.base import BaseRepository
from src.models.admin import AdminsOrm


class AdminRepository(BaseRepository[AdminsOrm]):
    def __init__(self):
        super().__init__(AdminsOrm)

    async def get_by_email(self, db: AsyncSession, email: str):
        result = await db.execute(select(self.model).where(self.model.email == email))
        return result.scalar_one_or_none()

    async def get_admin_with_hashed_password(self, db: AsyncSession, email: str):
        result = await db.execute(select(self.model).where(self.model.email == email))
        model = result.scalar_one_or_none()
        if model:
            return AdminWithHashedPassword.model_validate(model)
        return None

    async def update_last_login(self, db: AsyncSession, admin_id: int):
        from datetime import datetime
        admin = await self.get(db, admin_id)
        if admin:
            admin.last_login = datetime.utcnow()
            await db.commit()
