import logging
import typing as tp

from aiogram import executor
from aiogram import Dispatcher, types
from aiogram.types import BotCommand

from django.core.management.base import BaseCommand

from api.telegram_bot.loader import dp
from ommy_polland.settings import ADMINS_CHAT_IDS


async def on_startup_notify(dispatcher: Dispatcher) -> None:
    """
    Send message to admins when bot started
    Args:
         dispatcher: Dispatcher
    """

    for admin in ADMINS_CHAT_IDS:
        try:
            await dispatcher.bot.send_message(admin, "Бот Запущен")
        except Exception as err:
            logging.exception(err)


async def on_shutdown_notify(dispatcher: Dispatcher) -> None:
    """
    Send message to admins when bot stoped
    Args:
         dispatcher: Dispatcher
    """

    for admin in ADMINS_CHAT_IDS:
        try:
            await dp.bot.send_message(chat_id=admin, text="Я все( Остановился почемуто")
        except Exception as err:
            logging.exception(err)


async def create_default_commands() -> tp.List[BotCommand]:
    list_with_commands = [
        types.BotCommand('start', 'Запустить бота'),
        types.BotCommand('update_profile', 'Обновить профиль'),
        types.BotCommand('not_receive_orders', 'Остановить получение заказов'),
        types.BotCommand('receive_orders', 'Возобновить получение заказов'),
        types.BotCommand('feedback', 'Отправить сообщение администраторам, только после прохождении регеистрации'),
    ]
    return list_with_commands


async def set_default_commands(dispatcher: Dispatcher) -> None:
    """
    Set default commands
    Args:
         dispatcher: Dispatcher
    """

    list_with_commands = await create_default_commands()

    await dispatcher.bot.set_my_commands(list_with_commands)


async def on_startup(dispatcher: Dispatcher) -> None:
    """
    Set start up commands for bot
    """

    await set_default_commands(dispatcher=dispatcher)

    await on_startup_notify(dispatcher=dispatcher)


async def on_shutdown(dispatcher) -> None:
    """
    When bot stop
    """

    await on_shutdown_notify(dispatcher)


class Command(BaseCommand):
    """
    Run bot
    """

    help = 'Run telegram bot'

    def handle(self, *args, **options) -> None:
        executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
