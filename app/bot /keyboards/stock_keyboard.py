from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


buy_callback = CallbackData('buy', 'name', 'name_off', 'price', 'count', 'action', sep='~')


def create_kb_stock_switch(name, name_off, price, count):
    global buy_callback
    b1 = InlineKeyboardButton(text='Подробнее', callback_data=buy_callback.new(name=name, name_off=name_off, price=price, count=count, action='buy_switch'))
    kb_stock = InlineKeyboardMarkup(resize_keyboard=True)
    kb_stock.row(b1)
    return kb_stock


def create_kb_stock(name, name_off, price, count):
    global buy_callback
    b1 = InlineKeyboardButton(text='+', callback_data=buy_callback.new(name=name, name_off=name_off, price=price, count=count, action='+'))
    b2 = InlineKeyboardButton(text='-',
                              callback_data=buy_callback.new(name=name, name_off=name_off, price=price, count=count,
                                                             action='-'))
    b3 = InlineKeyboardButton(text='Купить', callback_data=buy_callback.new(name=name, name_off=name_off, price=price, count=count, action='buy'))
    b4 = InlineKeyboardButton(text='Личный кабинет',
                              callback_data=buy_callback.new(name=1, name_off=1, price=1, count=1,
                                                             action='cabinet'))
    b5 = InlineKeyboardButton(text='Новости',
                              callback_data=buy_callback.new(name=1, name_off=1, price=1, count=1,
                                                             action='cabinet'))
    b6 = InlineKeyboardButton(text='Идеи',
                              callback_data=buy_callback.new(name=1, name_off=1, price=1, count=1,
                                                             action='cabinet'))
    b7 = InlineKeyboardButton(text='Последний отчёт',
                              callback_data=buy_callback.new(name=1, name_off=1, price=1, count=1,
                                                             action='cabinet'))
    kb_stock = InlineKeyboardMarkup(resize_keyboard=True)
    kb_stock.row(b1, b2, b3)
   # kb_stock.row(b5, b6, b7)
    kb_stock.add(b4)
    return kb_stock

