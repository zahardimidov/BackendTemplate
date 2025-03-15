import json

from app.config import TEST_MODE
from app.exceptions import UnauthorizedException
from app.infra.database.models import User
from app.infra.repository import UserRepository
from app.schemas import UserMe
from app.utils.security import create_jwt_token, verify_jwt_token
from app.utils.telegram import validate_init_data


class UserService:
    def __init__(self):
        self.repo = UserRepository()

    async def get_by_id(self, user_id: int):
        return await self.repo.get(user_id)

    async def create_or_update(self, user_id: int, **data):
        user = await self.repo.get(user_id)

        if not user:
            return await self.repo.create(id=user_id, **data)
        return await self.repo.update(id=user_id, **data)

    async def authenticate_telegram_user(self, init_data: str) -> str:
        parsed_data = validate_init_data(init_data)

        if not parsed_data:
            raise UnauthorizedException

        user_info: dict = json.loads(parsed_data["user"])

        user = UserMe(
            user_id=int(user_info["id"]),
            username=user_info.get("username"),
            first_name=user_info.get("first_name")
        )

        return await self.authenticate_user(user)

    async def authenticate_user(self, user: UserMe) -> str:
        user = await self.create_or_update(**user.model_dump())
        auth_token = create_jwt_token(data={"user_id": user.id})

        return auth_token

    async def get_authenticated_user(self, token: str) -> User:
        decoded_data = verify_jwt_token(token)

        if TEST_MODE and token.isdigit() and not decoded_data:
            decoded_data = {"user_id": token}
        elif not decoded_data:
            raise UnauthorizedException

        user = await self.get_by_id(int(decoded_data["user_id"]))
        if not user:
            raise UnauthorizedException

        return user
