from aiogram.utils.executor import start_polling
from django.core.management.base import BaseCommand
from ugc.loader import bot, storage
from ugc.handlers import dp
# import filters
# import middlewares


class Command(BaseCommand):
    """ Класс для запуска бота в management commands Django """
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)


async def on_startup(dp):
    pass
    # filters.setup(dp)
    # middlewares.setup(dp)


async def on_shutdown(dp):
    await bot.close()
    await storage.close()
