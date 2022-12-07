from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


switch_market_buy_callback = CallbackData('buy', 'count', 'cur', 'q', 'action', sep='~')


def create_kb_market_switch(cur, count, q):
    kb_market_switch = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton(text='+',
                              callback_data=switch_market_buy_callback.new(count=count, cur=cur, q=q,
                                                                       action='+'))
    b2 = InlineKeyboardButton(text='-',
                              callback_data=switch_market_buy_callback.new(count=count, cur=cur, q=q,
                                                                       action='-'))
    b3 = InlineKeyboardButton(text='Купить',
                              callback_data=switch_market_buy_callback.new(count=count, cur=cur, q=q,
                                                                       action='buy_ser'))
    b4 = InlineKeyboardButton(text='←',
                                  callback_data=switch_market_buy_callback.new(count=count, cur=cur, q=q,
                                                                 action='left'))
    b5 = InlineKeyboardButton(text='→',
                                  callback_data=switch_market_buy_callback.new(count=count, cur=cur, q=q,
                                                                 action='right'))
    b6 = InlineKeyboardButton(text='Назад',
                                  callback_data=switch_market_buy_callback.new(count=count, cur=cur, q=q,
                                                                 action='back'))
    kb_market_switch.row(b1, b2, b3)
    kb_market_switch.row(b4, b5)
    kb_market_switch.add(b6)
    return kb_market_switch


