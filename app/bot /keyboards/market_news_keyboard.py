from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


kb_news_callback = CallbackData('buy', 'cur', 'action', sep='~')


def create_kb_market_news(cur=0):
    kb_market_news = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton(text='←',
                                  callback_data=kb_news_callback.new(cur=cur,
                                                                 action='left'))
    b2 = InlineKeyboardButton(text='→',
                                  callback_data=kb_news_callback.new(cur=cur,
                                                                 action='right'))
    b3 = InlineKeyboardButton(text='Назад',
                                  callback_data=kb_news_callback.new(cur=cur,
                                                                 action='back'))
    kb_market_news.row(b1, b2)
    kb_market_news.add(b3)
    return kb_market_news


