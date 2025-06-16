from aiogram import Bot, Dispatcher
from core.config import read_config
import logging
from .handlers import register_handlers

API_TOKEN = read_config().bot_token

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
register_handlers(dp)

async def start_bot():
    logging.info('Запуск Telegram-бота')
    await dp.start_polling(bot)