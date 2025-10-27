from fastapi import APIRouter, Request, Response

from src.utils.dependencies import AdminIdDep, DBDep
from src.schemas.admin import AdminRequestAdd, AdminResponse
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
    IncorrectTokenException
)


router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/register", summary="Регистрация нового администратора")
async def register_admin(
    data: AdminRequestAdd,
    db: DBDep,
):
    try:
        await AdminService(db).register_admin(data)
    except AdminAlreadyExistsException:
        raise AdminEmailAlreadyExistsHTTPException()
    return {"detail": "Вы успешно зарегистрировались!"}


@router.post("/login", summary="Вход администратора в систему")
async def login_admin(
    data: AdminRequestAdd,
    response: Response,
    request: Request,
    db: DBDep,
):
    token = request.cookies.get("access_token")
    if token:
        try:
            AdminService(db).decode_token(token)
            raise AdminIsAlreadyAuthenticatedHTTPException()
        except ExpiredTokenException:
            pass
        except IncorrectTokenException:
            pass

    try:
        access_token = await AdminService(db).login_admin(data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException()
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException()

    response.set_cookie("access_token", access_token)
    return {"detail": "Успешный вход в систему!", "access_token": access_token}


@router.get("/me", summary="Получение текущего администратора в системе", response_model=AdminResponse)
async def get_me(
    admin_id: AdminIdDep,
    db: DBDep,
):
    return await AdminService(db).get_one_or_none_admin(admin_id)


@router.post("/logout", summary="Выход из системы", response_model=None)
async def logout_admin(response: Response, request: Request, db: DBDep):
    token = request.cookies.get("access_token")
    try:
        await AdminService(db).logout_admin(token)
    except AdminNotAuthenticatedException:
        raise AdminNotAuthenticatedHTTPException()

    response.delete_cookie("access_token")
    return {"detail": "Вы вышли из системы!"}
