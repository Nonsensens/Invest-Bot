from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('💎Войти')

kb_start = ReplyKeyboardMarkup(resize_keyboard=True)
kb_start.add(b1)
