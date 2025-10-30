from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.dependencies import AdminIdDep, DBDep
from src.schemas.admin import Admin, AdminRequestAdd, AdminRequestLogin, AdminResponse
from src.services.admin import AdminService
from src.exceptions import (
    AdminAlreadyExistsException,
    AdminEmailAlreadyExistsHTTPException,
    AdminIsAlreadyAuthenticatedHTTPException,
    AdminNotAuthenticatedException,
    AdminNotAuthenticatedHTTPException,
    EmailNotRegisteredException,
    EmailNotRegisteredHTTPException,
    ExpiredTokenException,
    IncorrectPasswordException,
    IncorrectPasswordHTTPException,
    IncorrectTokenException,
    SuperadminPasswordException,
    SuperadminPasswordHTTPException
)

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/register", summary="Регистрация нового администратора")
async def register_admin(
    data: AdminRequestAdd,
    request: Request,
    db: DBDep,
):
    token = request.cookies.get("access_token")
    if token:
        try:
            AdminService(db).verify_token(token)
            raise AdminIsAlreadyAuthenticatedHTTPException()
        except (ExpiredTokenException, IncorrectTokenException):
            pass

    try:
        await AdminService(db).register_admin(data)
    except AdminAlreadyExistsException:
        raise AdminEmailAlreadyExistsHTTPException()
    except SuperadminPasswordException:
        raise SuperadminPasswordHTTPException()
    return {"detail": "Вы успешно зарегистрировались!"}


@router.post("/login", summary="Вход администратора в систему", response_model=dict)
async def login_admin(
    data: AdminRequestLogin,
    response: Response,
    request: Request,
    db: DBDep,
):
    token = request.cookies.get("access_token")
    if token:
        try:
            AdminService(db).verify_token(token)
            raise AdminIsAlreadyAuthenticatedHTTPException()
        except (ExpiredTokenException, IncorrectTokenException):
            pass

    try:
        access_token = await AdminService(db).login_admin(data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException()
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException()

    response.set_cookie("access_token", access_token)
    return {"detail": "Успешный вход в систему!", "access_token": access_token}


@router.get("/me", summary="Получение текущего администратора в системе", response_model=Admin)
async def get_me(
    admin_id: AdminIdDep,
    db: DBDep,
):
    return await AdminService(db).get_one_or_none_admin(admin_id)


@router.post("/logout", summary="Выход из системы", response_model=dict)
async def logout_admin(
    response: Response,
    request: Request,
    db: DBDep
):
    token = request.cookies.get("access_token")
    try:
        await AdminService(db).logout_admin(token)
    except AdminNotAuthenticatedException:
        raise AdminNotAuthenticatedHTTPException()

    response.delete_cookie("access_token")
    return {"detail": "Вы вышли из системы!"}
