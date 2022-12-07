from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('Вернуться назад')


kb_profile_back = ReplyKeyboardMarkup(resize_keyboard=True)
kb_profile_back.add(b1)
