from fastapi import HTTPException


class HandmadeException(Exception):
    detail = "Неожиданная ошибка!"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(HandmadeException):
    detail = "Объект не найден!"


class HandmadeHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)
