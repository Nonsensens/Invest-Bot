from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from keyboards.client_keyboards import client_keyboard
from handlers.entrance import User


async def client_handler_game(message: types.message):
    await message.answer('👈', reply_markup=client_keyboard.kb_client)
    await User.user.set()


def register_client_game_handler(dp: Dispatcher):
    dp.register_message_handler(client_handler_game, Text(equals='Назад'), state='*')