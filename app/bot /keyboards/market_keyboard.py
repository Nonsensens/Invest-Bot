from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

market_callback = CallbackData('market', 'action', sep='~')
b1 = InlineKeyboardButton(text='🔮Глобальный поиск', callback_data=market_callback.new(action='search'))
b2 = InlineKeyboardButton(text='💥Что купить?', callback_data=market_callback.new(action='suggestions'))
b3 = InlineKeyboardButton(text='📰Новости', callback_data=market_callback.new(action='news'))
b4 = InlineKeyboardButton(text='Назад', callback_data=market_callback.new(action='back'))
kb_market = InlineKeyboardMarkup(resize_keyboard=True)
kb_market.add(b1)
kb_market.row(b2, b3)
kb_market.add(b4)

