from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('1')
b2 = KeyboardButton('2')
b3 = KeyboardButton('3')
b4 = KeyboardButton('4')

kb_client_profile = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_profile.row(b1, b2, b3, b4)
