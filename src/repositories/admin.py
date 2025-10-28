from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.admin import AdminWithHashedPassword
from src.repositories.mappers.mappers import AdminDataMapper
from src.repositories.base import BaseRepository
from src.models.admin import AdminsOrm


class AdminRepository(BaseRepository[AdminsOrm]):
    def __init__(self, session: AsyncSession):
        super().__init__(AdminsOrm, session)

    model = AdminsOrm
    mapper = AdminDataMapper

    async def get_by_email(self, email: str):
        """Получить администратора по email"""
        result = await self.session.execute(
            select(self.model).where(self.model.email == email)
        )
        return result.scalar_one_or_none()

    async def get_admin_with_hashed_password(self, email: str):
        """Получить администратора с хешированным паролем"""
        result = await self.session.execute(
            select(self.model).where(self.model.email == email)
        )
        model = result.scalar_one_or_none()
        if model:
            return AdminWithHashedPassword.model_validate(model)
        return None

    async def update_last_login(self, admin_id: int) -> None:
        """Обновить время последнего входа"""
        from datetime import datetime

        admin = await self.get(admin_id)
        if admin:
            admin.last_login = datetime.utcnow()
            await self.session.commit()
