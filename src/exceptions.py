from fastapi import HTTPException


class HandmadeException(Exception):
    detail = "Неожиданная ошибка!"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(HandmadeException):
    detail = "Объект не найден!"


class ObjectAlreadyExistsException(HandmadeException):
    detail = "Похожий объект уже существует!"


class ExpiredTokenException(HandmadeException):
    detail = "Токен доступа истёк!"


class IncorrectTokenException(HandmadeException):
    detail = "Некорректный токен!"


class AdminAlreadyExistsException(HandmadeException):
    detail = "Администратор уже существует!"


class EmailNotRegisteredException(HandmadeException):
    detail = "Администратор с таким email не зарегистрирован!"


class AdminNotAuthenticatedException(HandmadeException):
    detail = "Вы не в системе, выход невозможен!"


class IncorrectPasswordException(HandmadeException):
    detail = "Пароль неверный!"


class SuperadminPasswordException(HandmadeException):
    detail = "Пароль суперадмина неверный!"


class HandmadeHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class AdminIsAlreadyAuthenticatedHTTPException(HandmadeHTTPException):
    status_code = 401
    detail = "Вы уже вошли в систему!"


class ExpiredTokenHTTPException(HandmadeHTTPException):
    status_code = 401
    detail = "Токен доступа истёк!"


class AdminEmailAlreadyExistsHTTPException(HandmadeHTTPException):
    status_code = 409
    detail = "Администратор с такой почтой уже существует!"


class EmailNotRegisteredHTTPException(HandmadeHTTPException):
    status_code = 401
    detail = "Администратор с таким email не зарегистрирован!"


class IncorrectPasswordHTTPException(HandmadeHTTPException):
    status_code = 401
    detail = "Пароль неверный!"


class IncorrectTokenHTTPException(HandmadeHTTPException):
    status_code = 401
    detail = "Некорректный токен!"


class NoAccessTokenHTTPException(HandmadeHTTPException):
    status_code = 401
    detail = "Вы не предоставили токен доступа!"


class AdminNotAuthenticatedHTTPException(HandmadeHTTPException):
    status_code = 401
    detail = "Вы не в системе, выход невозможен!"


class SuperadminPasswordHTTPException(HandmadeHTTPException):
    status_code = 403
    detail = "Неверный пароль суперадмина!"
