from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.database import get_async_session
from src.schemas.admins import AdminResponse
from src.services.admins import AdminService
from src.services.categories import CategoryService
from src.services.orders import OrderService
from src.services.products import ProductService


# Зависимости для подключения к БД
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Зависимость для получения сессии БД"""
    async for session in get_async_session():
        yield session


# Зависимости для сервисов
def get_admin_service() -> AdminService:
    return AdminService()


def get_category_service() -> CategoryService:
    return CategoryService()


def get_product_service() -> ProductService:
    return ProductService()


def get_order_service() -> OrderService:
    return OrderService()


# Простая аутентификация для админки (можно заменить на JWT)
async def get_current_admin(
    admin_service: AdminService = Depends(get_admin_service),
    db: AsyncSession = Depends(get_db),
    token: str = None  # В реальном приложении через Header
) -> AdminResponse:
    """
    Простая аутентификация администратора.
    В реальном приложении заменить на JWT.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    # Временная реализация - проверяем существование администратора
    admin = await admin_service.get_by_username(db, "admin")
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    return admin


# Зависимость для проверки прав администратора
async def require_admin(
    current_admin: AdminResponse = Depends(get_current_admin)
) -> AdminResponse:
    """Зависимость, требующая аутентификации администратора"""
    return current_admin
