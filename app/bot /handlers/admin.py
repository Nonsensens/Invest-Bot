from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove
from keyboards.remove_user_inline_keyboard import create_remove_bt
import requests


class RemoveUser(StatesGroup):
    remove = State()


async def admin_handler_users(message: types.message, state: FSMContext):
    await state.set_state(RemoveUser.remove)
    if message.from_user.id == 750899598:
        content = requests.get('http://217.18.60.9/users').json()
        for i in content:
            await message.answer(i, reply_markup=create_remove_bt(i['tg_id']))


async def admin_handler_remove_user(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(f'Удалён {call.data[7:]}', reply_markup=ReplyKeyboardRemove())
    await state.finish()
    requests.put('http://217.18.60.9/remove', json={'tg_id': call.data[7:]})


def register_admin_handler(dp: Dispatcher):
    dp.register_message_handler(admin_handler_users, commands='users', state='*')
    dp.register_callback_query_handler(admin_handler_remove_user, state=RemoveUser.remove)

