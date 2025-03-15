from aiogram import Dispatcher
from aiogram.types import Update
from fastapi import Request

from app.bot.dialogs import setup_dialogs
from app.bot.middlewares import RegisterUserMiddleware
from app.bot.settings import bot
from app.config import WEBHOOK_URL


async def run_bot_webhook():
    me = await bot.get_me()
    print(me.username)

    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True, allowed_updates=["message", "edited_channel_post", "callback_query"])


async def run_bot_polling():
    me = await bot.get_me()
    print(me.username)

    await bot.delete_webhook(True)
    await dp.start_polling(bot)

dp = Dispatcher()
dp.message.middleware(RegisterUserMiddleware())

setup_dialogs(dp)


async def process_update(request: Request):
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
