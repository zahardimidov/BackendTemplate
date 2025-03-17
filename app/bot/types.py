from aiogram import Bot as AiogramBot
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message as AiogramMessage
from aiogram.types import Update
from fastapi import Request

from app.logging import logger
from app.services import UserService


class Services:
    users = UserService()


class Bot(AiogramBot):
    def __init__(self, token, session=None, **kwargs):
        self.services = Services()
        self.dispatcher = Dispatcher()

        default = DefaultBotProperties(parse_mode=ParseMode.HTML)

        super().__init__(token, session, default, **kwargs)

    async def run_webhook(self, url: str):
        me = await self.get_me()
        logger.info(me.username)
        await self.set_webhook(
            url,
            drop_pending_updates=True,
            allowed_updates=["message", "edited_channel_post", "callback_query"],
        )

    async def run_polling(self):
        me = await self.get_me()
        logger.info(me.username)

        await self.delete_webhook(True)
        await self.dispatcher.start_polling(self)

    async def process_update(self, request: Request):
        update = Update.model_validate(await request.json(), context={"bot": self})
        await self.dispatcher.feed_update(self, update)


class Message(AiogramMessage):
    bot: Bot
