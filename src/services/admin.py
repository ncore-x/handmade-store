import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.admin import AdminRepository
from src.schemas.admin import AdminRequestAdd, AdminResponse
from src.config import settings
from src.exceptions import (
    AdminAlreadyExistsException,
    AdminNotAuthenticatedException,
    EmailNotRegisteredException,
    ExpiredTokenException,
    IncorrectPasswordException,
    IncorrectTokenException,
    SuperadminPasswordException
)


class AdminService:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.repository = AdminRepository(db_manager.session)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def _verify_superadmin_password(self, provided_password: str) -> bool:
        """Проверка пароля суперадмина"""
        return provided_password == settings.SUPERADMIN_PASSWORD

    def create_access_token(self, data: dict) -> str:
        """Создание JWT токена с RS256"""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode,
            settings.JWT_PRIVATE_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_token(self, token: str) -> dict:
        """Декодирование токена с RS256"""
        try:
            return jwt.decode(
                token,
                settings.JWT_PUBLIC_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
        except jwt.ExpiredSignatureError:
            raise ExpiredTokenException()
        except jwt.InvalidTokenError:
            raise IncorrectTokenException()

    async def register_admin(self, data: AdminRequestAdd) -> AdminResponse:
        """Регистрация администратора с проверкой пароля суперадмина"""
        if not self._verify_superadmin_password(data.superadmin_password):
            raise SuperadminPasswordException()

        existing_admin = await self.repository.get_by_email(data.email)
        if existing_admin:
            raise AdminAlreadyExistsException()

        admin_dict = {
            "email": data.email,
            "hashed_password": self.hash_password(data.password),
            "updated_at": datetime.utcnow()
        }

        admin = await self.repository.create(admin_dict)
        return AdminResponse.model_validate(admin)

    async def login_admin(self, data: AdminRequestAdd) -> str:
        """Аутентификация администратора"""
        admin = await self.repository.get_admin_with_hashed_password(data.email)

        if not admin:
            raise EmailNotRegisteredException()

        if not self.verify_password(data.password, admin.hashed_password):
            raise IncorrectPasswordException()

        await self.repository.update_last_login(admin.id)

        access_token = self.create_access_token(
            {"admin_id": admin.id, "sub": admin.email})
        return access_token

    async def logout_admin(self, token: str):
        """Выход из системы"""
        if not token:
            raise AdminNotAuthenticatedException()
        try:
            self.decode_token(token)
        except IncorrectTokenException:
            raise AdminNotAuthenticatedException()

    async def get_one_or_none_admin(self, admin_id: int) -> AdminResponse:
        """Получить администратора по ID"""
        admin = await self.repository.get(admin_id)
        if not admin:
            raise AdminNotAuthenticatedException()
        return AdminResponse.model_validate(admin)
