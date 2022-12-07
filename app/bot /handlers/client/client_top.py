import requests
from aiogram import types, Dispatcher
from aiogram.types import InputFile, InputMediaPhoto
from keyboards.client_keyboards import client_keyboard
from keyboards.top_keyboard import create_kb_top, top_callback
from handlers.client.get_price import get_price


strs = dict()


async def client_handler_top(call: types.CallbackQuery):
    global strs
    data = call.data.split('~')
    cur = 0
    if data[-1] == 'left' or data[-1] == 'right':
        cur = int(data[1])
        if data[-1] == 'left' and (cur - 1) >= 0:
            cur -= 1
        elif data[-1] == 'left' and (cur - 1) < 0:
            cur = len(strs) - 1
        if data[-1] == 'right' and (cur + 1) <= len(strs) - 1:
            cur += 1
        elif data[-1] == 'right' and (cur + 1) > len(strs) - 1:
            cur = 0
        photo = strs[cur][cur][1]
        if strs[cur][cur][1] == 'default':
            photo = InputFile('/root/investBot/app/bot /templates/investor_demo.png')
        await call.message.edit_media(InputMediaPhoto(photo))
        await call.message.edit_caption(strs[cur][cur][0], parse_mode='html', reply_markup=create_kb_top(cur=cur))
        return
    content = requests.get('http://217.18.60.9/users').json()
    dict = {1: '🥇', 2: '🥈', 3: '🥉'}
    k = 1
    users = {}
    photos = {}
    for i in content:
        account = float(i['account'].replace(',', '.'))
        account_brokerage = account
        for stock in requests.get('http://217.18.60.9/stocks', json={'tg_id': i['tg_id']}).json():
            try:
                price = float(stock['price'])
            except:
                price = 0
            try:
                account_brokerage += price * stock['count']
            except:
                pass
        if i['photo'] == 'default':
            photo = 'default'
        else:
            photo = i['photo']
        if k <= 3:
            st = f'{i["name"]} {i["surname"]} {round(account_brokerage, 2)}$'
            users[st] = round(account_brokerage, 2)
            photos[st] = photo
        else:
            st = f'{i["name"]} {i["surname"]} {round(account_brokerage, 2)}$'
            users[st] = round(account_brokerage, 2)
            photos[st] = photo
        k += 1
    new_sorted_dictionary = {k: v for k, v in sorted(users.items(), key=lambda item: item[1])}
    k = 1
    u = 0
    strs = list()
    for i in reversed(new_sorted_dictionary):
        b = i
        if k < 4:
            st = f'<b>{dict[k]} {k} место: {i}</b>'
        else:
            st = f'{k} место: ' + i
        strs.append({u: [st, photos[b]]})
        u += 1
        k += 1
    photo = strs[cur][cur][1]
    if strs[cur][cur][1] == 'default':
        photo = InputFile('/root/investBot/app/bot /templates/investor_demo.png')
    await call.message.edit_media(InputMediaPhoto(photo))
    await call.message.edit_caption(strs[cur][cur][0], parse_mode='html', reply_markup=create_kb_top(cur=cur))


async def client_handler_top_back(call: types.CallbackQuery):
    photo = InputFile('/root/investBot/app/bot /templates/main_demo.jpg')
    await call.message.edit_media(InputMediaPhoto(photo))
    await call.message.edit_caption(caption='<b>Личный кабинет</b>', reply_markup=client_keyboard.kb_client,
                                    parse_mode='html')


def register_client_top_handler(dp: Dispatcher):
    dp.register_callback_query_handler(client_handler_top, client_keyboard.client_callback.filter(choose='top'),
                                       state='*')
    dp.register_callback_query_handler(client_handler_top,
                                       top_callback.filter(action='left'),
                                       state='*')
    dp.register_callback_query_handler(client_handler_top,
                                       top_callback.filter(action='right'),
                                       state='*')
    dp.register_callback_query_handler(client_handler_top_back,
                                       top_callback.filter(action='back'),
                                       state='*')

