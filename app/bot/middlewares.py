from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware

from app.bot.types import Message


class RegisterUserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str: Any],
    ) -> Any:

        if not event.chat.type == 'private':
            return

        user = await event.bot.services.users.get_by_id(user_id=event.from_user.id)

        if not user:
            user = await event.bot.services.users.create_or_update(
                id=event.from_user.id,
                username=event.from_user.username
            )

        data['user'] = user

        return await handler(event, data)
