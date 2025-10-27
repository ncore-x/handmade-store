from typing import Annotated
from fastapi import Depends, Query, Request
from pydantic import BaseModel

from src.utils.database import async_session_maker
from src.services.admin import AdminService
from src.services.category import CategoryService
from src.services.order import OrderService
from src.services.product import ProductService
from src.utils.db_manager import DBManager
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


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise NoAccessTokenHTTPException()
    return token


def get_current_admin_id(
    token: str = Depends(get_token),
    db: DBManager = Depends(lambda: DBManager(
        session_factory=async_session_maker)),
) -> int:
    try:
        payload = AdminService(db).decode_token(token)
    except ExpiredTokenException:
        raise ExpiredTokenHTTPException
    except IncorrectTokenException:
        raise IncorrectTokenHTTPException()

    admin_id = payload.get("admin_id")
    if not admin_id:
        raise IncorrectTokenHTTPException()
    return admin_id


PaginationDep = Annotated[PaginationParams, Depends()]
AdminIdDep = Annotated[int, Depends(get_current_admin_id)]
DBDep = Annotated[DBManager, Depends(get_db)]
