import logging
import unittest

from app.services.user import UserService
from tests.data import USER
from tests.unit.context import Context


class TestUserService(unittest.IsolatedAsyncioTestCase, metaclass=Context):
    def __init__(self, methodName="runTest"):
        self.service = UserService()
        super().__init__(methodName)

    async def test_auth(self):
        token = await self.service.authenticate_user(USER)

        logging.info(f'{token=}')

        user = await self.service.get_authenticated_user(token=token)

        assert user.id == USER.user_id
