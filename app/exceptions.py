from fastapi import HTTPException


class ServiceException(HTTPException):
    ...


class UnauthorizedException(ServiceException):
    def __init__(self, detail="Пользователь не авторизован", headers=None):
        super().__init__(401, detail, headers)
