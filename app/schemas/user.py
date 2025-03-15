
from pydantic import Field

from .base import BaseModel, RequestModel


class UserSignIn(RequestModel):
    init_data: str = Field(description='Значение window.Telegram.WebApp.initData')


class UserSignInResponse(BaseModel):
    token: str = Field(description='JWT токен для авторизации пользователя')


class UserMe(BaseModel):
    user_id: int
    username: str | None
    first_name: str
