from typing import Annotated, AsyncGenerator
from fastapi import Depends, Query, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.database import async_session_maker
from src.services.admin import AdminService
from src.services.category import CategoryService
from src.services.order import OrderService
from src.services.product import ProductService
from src.exceptions import (
    ExpiredTokenException,
    ExpiredTokenHTTPException,
    IncorrectTokenException,
    IncorrectTokenHTTPException,
    NoAccessTokenHTTPException
)


class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(None, ge=1, lt=30)]


PaginationDep = Annotated[PaginationParams, Depends()]


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


DBDep = Annotated[AsyncSession, Depends(get_db)]


def get_admin_service(db: DBDep) -> AdminService:
    return AdminService(db)


def get_category_service(db: DBDep) -> CategoryService:
    return CategoryService(db)


def get_product_service(db: DBDep) -> ProductService:
    return ProductService(db)


def get_order_service(db: DBDep) -> OrderService:
    return OrderService(db)


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise NoAccessTokenHTTPException()
    return token


def get_current_admin_id(
    token: str = Depends(get_token),
    db: AsyncSession = Depends(get_db),
) -> int:
    try:
        admin_service = AdminService(db)
        admin_id = admin_service.verify_token(token)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException()
    except IncorrectTokenException:
        raise IncorrectTokenHTTPException()

    return admin_id


AdminIdDep = Annotated[int, Depends(get_current_admin_id)]
