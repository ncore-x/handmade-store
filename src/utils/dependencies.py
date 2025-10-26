from typing import Annotated, AsyncGenerator
from fastapi import Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.database import async_session_maker
from src.schemas.admin import AdminResponse
from src.services.admin import AdminService
from src.services.category import CategoryService
from src.services.order import OrderService
from src.services.product import ProductService
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(None, ge=1, lt=30)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


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


PaginationDep = Annotated[PaginationParams, Depends()]
AdminIdDep = Annotated[int, Depends(get_current_admin)]
DBDep = Annotated[DBManager, Depends(get_db)]
