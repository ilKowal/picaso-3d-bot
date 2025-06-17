from aiogram import Bot
from typing import Optional
from bot.keyboards.main_menu import get_main_keyboard

bot_instance: Optional[Bot] = None
chat_id: Optional[int] = None 

def setup(bot: Bot, target_chat_id: int):
    global bot_instance, chat_id
    bot_instance = bot
    chat_id = target_chat_id

async def send_message(text: str):
    if bot_instance and chat_id:
        await bot_instance.send_message(chat_id=chat_id, text=text, reply_markup=get_main_keyboard())
    else:
        print('[!] Бот не инициализирован или chat_id неизвестен')