from fastapi import FastAPI

from app.config import WEBHOOK_URL, WEBHOOK_PATH, BOT_TOKEN
from app.logging import logger

async def init_bot(app: FastAPI):
    if not BOT_TOKEN:
        return logger.info(f'Bot was not initialized: Token was not provided')
    
    from app.bot.settings import bot
    from app.bot.dialogs import setup_dialogs
    from app.bot.middlewares import RegisterUserMiddleware
    
    bot.dispatcher.message.middleware(RegisterUserMiddleware())
    setup_dialogs(bot.dispatcher)

    app.add_api_route(WEBHOOK_PATH, endpoint=bot.process_update, methods=['post'])
    await bot.run_webhook(WEBHOOK_URL)