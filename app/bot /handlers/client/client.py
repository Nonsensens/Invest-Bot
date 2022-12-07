from aiogram import types, Dispatcher
from keyboards.client_keyboards import client_keyboard
import time
import requests

bral = False
timer = time.time()


async def client_handler_gift(call: types.CallbackQuery):
    data = requests.get('http://217.18.60.9/profile',
                                   json={'tg_id': call.message.chat.id}).json()
    timer = float(data['timer'])
    first_gift = data['first_gift']
    if time.time() - timer >= 86400 or first_gift == 0:
        await call.answer('Подарок получен! +100$')
        account = float(data['account'])
        requests.put('http://217.18.60.9/profile', json={'tg_id': call.message.chat.id,
                                                            'account': str(account + 100),
                                                            'first_gift': True,
                                                            'timer': time.time()})
    else:
        time_passed = time.time() - timer
        time_left = 86400 - time_passed
        hours_left = time_left // 3600
        minutes_left = time_left // 60 % 60
        await call.answer(f'Доступен через {round(hours_left)}:{round(minutes_left)}')


def register_client_handler(dp: Dispatcher):
    dp.register_callback_query_handler(client_handler_gift, client_keyboard.client_callback.filter(choose='gift'),
                                       )
