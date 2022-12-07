from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


b1 = KeyboardButton(text='Пропустить')
kb_skip_photo = ReplyKeyboardMarkup(resize_keyboard=True)
kb_skip_photo.add(b1)

