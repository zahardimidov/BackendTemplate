from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.infra.database.models import User
from app.services import UserService

auth_scheme = HTTPBearer()


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    service: UserService = Depends(UserService),
):
    return await service.get_authenticated_user(token=token.credentials)

CurrentUser = Annotated[User, Depends(get_current_user)]
