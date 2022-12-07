from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

client_callback = CallbackData('action', 'choose', sep='~')

b1 = InlineKeyboardButton('😎Я', callback_data=client_callback.new(choose='me'))
b2 = InlineKeyboardButton('📈Мои активы', callback_data=client_callback.new(choose='stocks'))
b3 = InlineKeyboardButton('🎁Подарок', callback_data=client_callback.new(choose='gift'))
b4 = InlineKeyboardButton('🏆Таблица лидеров', callback_data=client_callback.new(choose='top'))
b5 = InlineKeyboardButton('💼Фондовый рынок', callback_data=client_callback.new(choose='market'))

kb_client = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
kb_client.insert(b1).insert(b2).insert(b3).insert(b4)
kb_client.add(b5)
