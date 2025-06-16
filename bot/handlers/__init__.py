from aiogram import Dispatcher
from . import commands

def register_handlers(dp: Dispatcher):
    dp.include_router(commands.router)