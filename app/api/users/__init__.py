from fastapi import APIRouter

from app.api.dependencies import CurrentUser
from app.schemas import UserMe

from .auth import router as auth_router

router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.get("/me", response_model=UserMe, summary="Получение профиля пользователем")
async def user_me(user: CurrentUser):
    return UserMe(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name
    )

router.include_router(auth_router)
