from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from src.repositories.admin import AdminRepository
from src.schemas.admin import AdminCreate, AdminUpdate, AdminResponse, AdminLogin
from src.services.base import BaseService

# Хеширование паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AdminService(BaseService):
    def __init__(self):
        super().__init__(AdminRepository())

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Проверить пароль"""
        return pwd_context.verify(plain_password, hashed_password)

    def _get_password_hash(self, password: str) -> str:
        """Получить хеш пароля"""
        return pwd_context.hash(password)

    async def authenticate(
        self,
        db: AsyncSession,
        login_data: AdminLogin
    ) -> Optional[AdminResponse]:
        """Аутентификация администратора"""
        admin = await self.repository.get_by_username(db, login_data.username)
        if not admin:
            return None

        if not self._verify_password(login_data.password, admin.hashed_password):
            return None

        # Обновляем время последнего входа
        await self.repository.update_last_login(db, admin.id)

        return AdminResponse.model_validate(admin)

    async def create(self, db: AsyncSession, obj_in: AdminCreate) -> AdminResponse:
        """Создать администратора с хешированием пароля"""
        # Проверяем уникальность username и email
        existing_admin = await self.repository.get_by_username(db, obj_in.username)
        if existing_admin:
            raise ValueError("Username already exists")

        existing_email = await self.repository.get_by_email(db, obj_in.email)
        if existing_email:
            raise ValueError("Email already exists")

        # Хешируем пароль
        obj_data = obj_in.model_dump()
        obj_data["hashed_password"] = self._get_password_hash(
            obj_data.pop("password"))

        db_obj = await self.repository.create(db, obj_data)
        return AdminResponse.model_validate(db_obj)

    async def get_by_username(self, db: AsyncSession, username: str) -> Optional[AdminResponse]:
        """Получить администратора по имени пользователя"""
        admin = await self.repository.get_by_username(db, username)
        if admin:
            return AdminResponse.model_validate(admin)
        return None

    async def update_password(
        self,
        db: AsyncSession,
        admin_id: int,
        new_password: str
    ) -> bool:
        """Обновить пароль администратора"""
        hashed_password = self._get_password_hash(new_password)
        admin = await self.repository.get(db, admin_id)
        if not admin:
            return False

        await self.repository.update(db, admin, {"hashed_password": hashed_password})
        return True
