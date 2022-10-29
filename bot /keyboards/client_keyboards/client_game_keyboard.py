from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('Назад')


kb_client_game = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_game.add(b1)
