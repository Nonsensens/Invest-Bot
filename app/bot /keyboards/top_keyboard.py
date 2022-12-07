from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


top_callback = CallbackData('back', 'cur', 'action', sep='~')


def create_kb_top(cur=0):
    kb_top = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton(text='←',
                                  callback_data=top_callback.new(cur=cur,
                                                                 action='left'))
    b2 = InlineKeyboardButton(text='→',
                                  callback_data=top_callback.new(cur=cur,
                                                                 action='right'))
    b3 = InlineKeyboardButton(text='Назад',
                                  callback_data=top_callback.new(cur=cur,
                                                                 action='back'))
    kb_top.row(b1, b2)
    kb_top.add(b3)
    return kb_top


