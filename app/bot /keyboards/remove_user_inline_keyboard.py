from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


def create_remove_bt(id):
    new_callback = CallbackData('remove', 'id')
    b1 = InlineKeyboardButton(text='Удалить', callback_data=new_callback.new(id=id))
    kb_remove = InlineKeyboardMarkup(resize_keyboard=True)
    kb_remove.add(b1)
    return kb_remove

