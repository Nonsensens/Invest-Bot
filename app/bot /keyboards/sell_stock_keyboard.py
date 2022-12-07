from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


sell_callback = CallbackData('sell', 'count', 'action', 'max_count', 'cur', sep='~')


def create_kb_sell_stock(count, max_count, cur):
    global sell_callback
    b1 = InlineKeyboardButton(text='+', callback_data=sell_callback.new(count=count, action='+', max_count=max_count, cur=cur))
    b2 = InlineKeyboardButton(text='-', callback_data=sell_callback.new(count=count, action='-', max_count=max_count, cur=cur))
    b3 = InlineKeyboardButton(text='Продать', callback_data=sell_callback.new(count=count, action='sell', max_count=max_count, cur=cur))
    b4 = InlineKeyboardButton(text='Подробнее', callback_data=sell_callback.new(max_count=max_count, count=1, action='sell_switch', cur=cur))
    b7 = InlineKeyboardButton(text='Назад',
                              callback_data=sell_callback.new(count='d', max_count='d', cur=cur,
                                                             action='back'))
    b5 = InlineKeyboardButton(text='←', callback_data=sell_callback.new(count=count, action='left',
                                                                        max_count=max_count,
                                                                        cur=cur))
    b6 = InlineKeyboardButton(text='→', callback_data=sell_callback.new(count=count, action='right',
                                                                        max_count=max_count, cur=cur))
    kb_sell_stock = InlineKeyboardMarkup(resize_keyboard=True)
    kb_sell_stock.row(b1, b2, b3)
    kb_sell_stock.row(b5, b6)
    kb_sell_stock.row(b4, b7)
    return kb_sell_stock

