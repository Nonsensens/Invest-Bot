from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

new_callback = CallbackData('number', 'digit')

b1 = InlineKeyboardButton(text='Имя', callback_data=new_callback.new(digit=1))
b2 = InlineKeyboardButton(text='Фамилия', callback_data=new_callback.new(digit=2))
b3 = InlineKeyboardButton(text='Фото', callback_data=new_callback.new(digit=3))
b4 = InlineKeyboardButton(text='Назад', callback_data=new_callback.new(digit=4))

kb_client_profile = InlineKeyboardMarkup(resize_keyboard=True)
kb_client_profile.row(b1, b2, b3)
kb_client_profile.add(b4)
