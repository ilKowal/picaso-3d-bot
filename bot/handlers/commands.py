from aiogram import Router, types
from aiogram.filters import Command
from core.status import get_status
from core.storage import load_previous_status
from core.output import take_status, take_progress, take_temperature, take_time, take_log
from core.printer.poller import PRINTER_IP, PRINTER_PORT, REQUEST_BYTES
from bot.keyboards.main_menu import get_main_keyboard
from bot.services.notifier import setup

router = Router()

@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer('Отслеживание событий запущено', reply_markup=get_main_keyboard())
    setup(message.bot, message.chat.id)

@router.message(Command('status'))
async def handle_status(message: types.Message):
    status = get_status(PRINTER_IP, PRINTER_PORT, REQUEST_BYTES)
    if status:
        text = take_status(status)
    else:
        status = load_previous_status()
        text = f'Устаревшие данные!!!\n{take_status(status)}'
    await message.answer(text, reply_markup=get_main_keyboard())
    await message.delete()

@router.message(Command('progress'))
async def handle_progress(message: types.Message):
    status = get_status(PRINTER_IP, PRINTER_PORT, REQUEST_BYTES)
    if status:
        text = take_progress(status)
    else:
        status = load_previous_status()
        text = f'Устаревшие данные!!!\n{take_progress(status)}'
    await message.answer(text, reply_markup=get_main_keyboard())
    await message.delete()

@router.message(Command('temperature'))
async def handle_temperature(message: types.Message):
    status = get_status(PRINTER_IP, PRINTER_PORT, REQUEST_BYTES)
    if status:
        text = take_temperature(status)
    else:
        status = load_previous_status()
        text = f'Устаревшие данные!!!\n{take_temperature(status)}'
    await message.answer(text, reply_markup=get_main_keyboard())
    await message.delete()

@router.message(Command('time'))
async def handle_time(message: types.Message):
    status = get_status(PRINTER_IP, PRINTER_PORT, REQUEST_BYTES)
    if status:
        text = take_time(status)
    else:
        status = load_previous_status()
        text = f'Устаревшие данные!!!\n{take_time(status)}'
    await message.answer(text, reply_markup=get_main_keyboard())
    await message.delete()

@router.message(Command('log'))
async def handle_log(message: types.Message):
    status = get_status(PRINTER_IP, PRINTER_PORT, REQUEST_BYTES)
    if status:
        text = take_log(status)
    else:
        status = load_previous_status()
        text = f'Устаревшие данные!!!\n{take_log(status)}'
    await message.answer(text, reply_markup=get_main_keyboard())
    await message.delete()

@router.message()
async def other_handler(message: types.Message):
    if message.text == 'Запуск':
        await cmd_start(message)
    elif message.text == 'Статус':
        await handle_status(message)
    elif message.text == 'Прогресс':
        await handle_progress(message)
    elif message.text == 'Время':
        await handle_time(message)
    elif message.text == 'Температура':
        await handle_temperature(message)
    elif message.text == 'Журнал':
        await handle_log(message)