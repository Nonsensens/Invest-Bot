from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


kb_suggestions_callback = CallbackData('sug', 'count', 'cur', 'action', sep='~')


def create_kb_market_suggestions(cur, count):
    kb_market_suggestions = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton(text='+',
                              callback_data=kb_suggestions_callback.new(count=count, cur=cur,
                                                                           action='+'))
    b2 = InlineKeyboardButton(text='-',
                              callback_data=kb_suggestions_callback.new(count=count, cur=cur,
                                                                           action='-'))
    b3 = InlineKeyboardButton(text='Купить',
                              callback_data=kb_suggestions_callback.new(count=count, cur=cur,
                                                                           action='buy_sug'))
    b4 = InlineKeyboardButton(text='←',
                              callback_data=kb_suggestions_callback.new(count=count, cur=cur,
                                                                           action='left'))
    b5 = InlineKeyboardButton(text='→',
                              callback_data=kb_suggestions_callback.new(count=count, cur=cur,
                                                                           action='right'))
    b6 = InlineKeyboardButton(text='Назад',
                              callback_data=kb_suggestions_callback.new(count=count, cur=cur,
                                                                           action='back'))
    kb_market_suggestions.row(b1, b2, b3)
    kb_market_suggestions.row(b4, b5)
    kb_market_suggestions.add(b6)
    return kb_market_suggestions


