from aiogram import Dispatcher, Router
from aiogram_dialog import ChatEvent
from aiogram_dialog import setup_dialogs as setup
from aiogram_dialog.api.internal.manager import DialogManagerFactory
from aiogram_dialog.api.protocols import DialogRegistryProtocol
from aiogram_dialog.context.media_storage import MediaIdStorage
from aiogram_dialog.manager.manager import ManagerImpl
from aiogram_dialog.manager.message_manager import MessageManager

from app.bot.settings import bot
from app.bot.types import Bot


class DialogManager(ManagerImpl):
    def __init__(self, event, message_manager, media_id_storage, registry, router, data):
        self.bot: Bot = bot

        super().__init__(event, message_manager, media_id_storage, registry, router, data)


class CustomManager(DialogManagerFactory):
    def __init__(
            self, **kwargs
    ) -> None:
        self.message_manager = MessageManager()
        self.media_id_storage = MediaIdStorage()

    def __call__(
            self, event: ChatEvent, data: dict,
            registry: DialogRegistryProtocol,
            router: Router,
    ) -> DialogManager:
        manager = DialogManager(
            event=event,
            data=data,
            message_manager=self.message_manager,
            media_id_storage=self.media_id_storage,
            registry=registry,
            router=router
        )

        return manager


custom_manager_factory = lambda **kwargs: CustomManager()(**kwargs)

dialogs = [

]


def setup_dialogs(dp: Dispatcher):
    for dialog in dialogs:
        dp.include_router(dialog)
    setup(dp, dialog_manager_factory=custom_manager_factory)
