from aiogram import Bot as AiogramBot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message as AiogramMessage

from app.services import UserService


class Services:
    users = UserService()


class Bot(AiogramBot):
    def __init__(self, token, session=None, **kwargs):
        self.services = Services()

        default = DefaultBotProperties(parse_mode=ParseMode.HTML)

        super().__init__(token, session, default, **kwargs)


class Message(AiogramMessage):
    bot: Bot
