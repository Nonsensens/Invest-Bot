from aiogram import types, Dispatcher
import requests


async def admin_handler_users(message: types.message):
    if message.from_user.id == 750899598:
        content = requests.get('http://127.0.0.1:5050/users').content
        await message.answer(content)


def register_admin_handler(dp: Dispatcher):
    dp.register_message_handler(admin_handler_users, commands='users', state='*')
