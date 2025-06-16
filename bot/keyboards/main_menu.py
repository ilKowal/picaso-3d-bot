from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard():
    btn1 = KeyboardButton(text='Запуск', callback_data='start')
    btn2 = KeyboardButton(text='Статус', callback_data='status')
    btn3 = KeyboardButton(text='Прогресс', callback_data='progress')
    btn4 = KeyboardButton(text='Время', callback_data='time')
    btn5 = KeyboardButton(text='Температура', callback_data='temperature')
    btn6 = KeyboardButton(text='Журнал', callback_data='log')
    kb = ReplyKeyboardMarkup(keyboard=[[btn1, btn2],[btn3, btn4], [btn5, btn6]], resize_keyboard=True)
    
    return kb