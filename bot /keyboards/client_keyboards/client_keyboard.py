from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('😎Я')
b2 = KeyboardButton('🎮Игра')
b3 = KeyboardButton('❌Выйти')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.add(b1).add(b2).add(b3)
