from aiogram import types, Dispatcher
from handlers.client import models_client
from handlers.entrance import User
from keyboards import start_keyboard
from keyboards.client_keyboards import client_profile_keyboard, client_game_keyboard
from aiogram.dispatcher import FSMContext
from create_bot import bot
import requests


async def client_handler_profile(message: types.message):
    t_id = {'tg_id': message.from_user.id}
    data = requests.get('http://127.0.0.1:5050/profile', json=t_id).json()
    await bot.send_photo(message.from_user.id, data["photo"], f'\n{data["name"]} {data["surname"]} - {data["status"]}\nДенег на счету: {data["account"]}', reply_markup=client_profile_keyboard.kb_client_profile)
    await message.answer('1. Заполнить профиль заново\n2. Изменить фото\n3. Изменить статус профиля\n4. Назад')
    await models_client.Profile.profile.set()


async def client_handler_game(message: types.message):
    await message.answer('In working', reply_markup=client_game_keyboard.kb_client_game)
    await models_client.Game.game.set()


async def client_handler_exit(message: types.message, state: FSMContext):
    await message.answer('Успешный выход🌚', reply_markup=start_keyboard.kb_start)
    await state.finish()


def register_client_handler(dp: Dispatcher):
    dp.register_message_handler(client_handler_profile, state=User.user, commands='Я', commands_prefix='😎')
    dp.register_message_handler(client_handler_game, state=User.user, commands='Игра', commands_prefix='🎮')
    dp.register_message_handler(client_handler_exit, state=User.user, commands='Выйти', commands_prefix='❌')
