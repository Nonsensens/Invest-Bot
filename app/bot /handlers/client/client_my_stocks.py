import requests
from aiogram import types, Dispatcher
from aiogram.types import InputFile, InputMediaPhoto
from keyboards.client_keyboards import client_keyboard
from keyboards.sell_stock_keyboard import create_kb_sell_stock, sell_callback
from keyboards.stock_keyboard import create_kb_stock
from bs4 import BeautifulSoup as bs


async def client_handler_see_stocks(call: types.CallbackQuery):
    data = call.data.split('~')
    stocks = requests.get('http://217.18.60.9/stocks', json={'tg_id': call.message.chat.id}).json()
    data.append('0')
    if data[1] == 'stocks':
        cur = 0
        max_count = int(stocks[cur]['count'])
        count = int(stocks[cur]['count'])
        price_old = float(stocks[cur]["price_old"].replace(",", "."))
        price = float(stocks[cur]["price"])
        name = stocks[cur]['name']
        name_off = stocks[cur]['name_off']
        photo = InputMediaPhoto(f'https://www.tradingview.com/symbols/{name_off.upper()}')
        if requests.get(f'https://www.tradingview.com/symbols/{stocks[cur]["name_off"].upper()}').status_code != 404:
            await call.message.edit_media(photo)
        else:
            await call.message.edit_media(
                InputMediaPhoto(InputFile('/root/investBot/app/bot /templates/stock_demo.jpg')))
        await call.message.edit_caption(
            parse_mode='html',
            caption=f'<b>{name} ({round(((price - price_old) / price_old) * 100, 2)} %)</b>\n'
                    f'Цена: <b>{round(price * count, 2)}$ ({count}x)</b>'
            , reply_markup=create_kb_sell_stock(cur=cur, count=count, max_count=max_count)
        )
        return
    if not stocks:
        await call.answer('Нет активов')
        return
    cur = int(data[-2])
    count = int(data[1])
    max_count = int(stocks[cur]['count'])
    action = data[2]
    if action == 'left' or action == 'right':
        if action == 'left':
            cur -= 1
        else:
            cur += 1
        if cur > len(stocks) - 1:
            cur = 0
        elif cur < 0:
            cur = len(stocks) - 1
    if data[2] == "-" and count - 1 < 1:
        count = count
    elif data[2] == "-" and count - 1 >= 1:
        count -= 1
    if data[2] == "+" and count + 1 <= max_count:
        count += 1
    elif data[2] == "+" and count + 1 > max_count:
        count = count
    if data[2] != '+' and data[2] != '-':
        count = int(stocks[cur]['count'])
        max_count = int(stocks[cur]['count'])
    price_old = float(stocks[cur]["price_old"].replace(",", "."))
    if price_old == 0:
        price_old = 0.001
    price = float(stocks[cur]["price"])
    name = stocks[cur]['name']
    name_off = stocks[cur]['name_off']
    photo = InputMediaPhoto(f'https://www.tradingview.com/symbols/{name_off.upper()}')
    if requests.get(f'https://www.tradingview.com/symbols/{stocks[cur]["name_off"].upper()}').status_code != 404:
        await call.message.edit_media(photo)
    else:
        await call.message.edit_media(
            InputMediaPhoto(InputFile('/root/investBot/app/bot /templates/stock_demo.jpg')))
    await call.message.edit_caption(
                         parse_mode='html',
                         caption=f'<b>{name} ({round(((price - price_old)/price_old)*100, 2)} %)</b>\n'
                                 f'Цена: <b>{round(price*count, 2)}$ ({count}x)</b>'
                              , reply_markup=create_kb_sell_stock(cur=cur, count=count, max_count=max_count)
        )


async def client_handler_sell_stocks(call: types.CallbackQuery):
    await call.answer('Продано')
    stocks = requests.get('http://217.18.60.9/stocks', json={'tg_id': call.message.chat.id}).json()
    data = call.data.split('~')
    count = int(data[1])
    cur = int(data[-1])
    count_max = int(stocks[cur]['count'])
    price_old = float(stocks[cur]["price_old"].replace(",", "."))
    if price_old == 0:
        price_old = 0.001
    price = float(stocks[cur]["price"])
    name = stocks[cur]['name']
    if count_max - count == 0:
        account = float(requests.get('http://217.18.60.9/profile', json={'tg_id': call.message.chat.id}).json()[
                            'account'].replace(',', '.'))
        requests.put('http://217.18.60.9/profile',
                     json={'tg_id': call.message.chat.id, 'account': str(round(account + price * count, 2))})
        requests.put('http://217.18.60.9/sellstock', json={'tg_id': call.from_user.id, 'name': name})
        if not (requests.get('http://217.18.60.9/stocks', json={'tg_id': call.message.chat.id}).json()):
            photo = InputFile('/root/investBot/app/bot /templates/main_demo.jpg')
            await call.message.edit_media(InputMediaPhoto(photo))
            await call.message.edit_caption(caption='<b>Личный кабинет</b>', reply_markup=client_keyboard.kb_client,
                                            parse_mode='html')
            return
        cur -= 1
        price_old = float(stocks[cur]["price_old"].replace(",", "."))
        if price_old == 0:
            price_old = 0.001
        price = float(stocks[cur]["price"])
        name = stocks[cur]['name']
        count_max = int(stocks[cur]['count'])
        count = int(stocks[cur]['count'])
        name_off = stocks[cur]['name_off']
        photo = InputMediaPhoto(f'https://www.tradingview.com/symbols/{name_off.upper()}')
        if requests.get(f'https://www.tradingview.com/symbols/{stocks[cur]["name_off"].upper()}').status_code != 404:
            await call.message.edit_media(photo)
        else:
            await call.message.edit_media(
                InputMediaPhoto(InputFile('/root/investBot/app/bot /templates/stock_demo.jpg')))
        await call.message.edit_caption(
            parse_mode='html',
            caption=f'<b>{name} ({round(((price - price_old) / price_old) * 100, 2)} %)</b>\n'
                    f'Цена: <b>{round(price * count, 2)}$ ({count}x)</b>'
            , reply_markup=create_kb_sell_stock(cur=cur, count=count, max_count=count_max)
        )
    else:
        name_off = stocks[cur]['name_off']
        photo = InputMediaPhoto(f'https://www.tradingview.com/symbols/{name_off.upper()}')
        account = float(requests.get('http://217.18.60.9/profile', json={'tg_id': call.message.chat.id}).json()[
                            'account'].replace(',', '.'))
        requests.put('http://217.18.60.9/profile',
                     json={'tg_id': call.message.chat.id, 'account': str(round(account + price * count, 2))})
        requests.put('http://217.18.60.9/stocks', json={'tg_id': call.from_user.id, 'name_off': name_off, 'count': count_max - count})
        if requests.get(f'https://www.tradingview.com/symbols/{stocks[cur]["name_off"].upper()}').status_code != 404:
            await call.message.edit_media(photo)
        else:
            await call.message.edit_media(
                InputMediaPhoto(InputFile('/root/investBot/app/bot /templates/stock_demo.jpg')))
        await call.message.edit_caption(
            parse_mode='html',
            caption=f'<b>{name} ({round(((price - price_old) / price_old) * 100, 2)} %)</b>\n'
                    f'Цена: <b>{round(price * (count_max - count), 2)}$ ({count_max - count}x)</b>'
            , reply_markup=create_kb_sell_stock(cur=cur, count=count_max - count, max_count=count_max - count))


async def inline_sell_switch(call: types.CallbackQuery):
    def get_info(symbol):
        try:
            r = requests.get(f'https://www.tinkoff.ru/invest/stocks/{symbol}/')
            html = bs(r.content, 'html.parser')
            about = html.find('h1', {'class': "SecurityBlockHeader__title_KUEiP"}).text
            about_sub = html.find('div', {'data-qa-file': "SecurityInfo"}).text
            about_sub = about_sub.split('.')
            about_sub.pop(-1)
            about_sub = '.'.join(about_sub)
            str = '<b>' + about + '</b>' + '\n' + about_sub
            return str
        except:
            return '<b>' + symbol + '</b>'

    stocks = requests.get('http://217.18.60.9/stocks', json={'tg_id': call.message.chat.id}).json()
    data = call.data.split('~')
    count = int(data[1])
    cur = int(data[-1])
    price = float(stocks[cur]["price"])
    name = stocks[cur]['name']
    name_off = stocks[cur]['name_off']
    photo = InputMediaPhoto(f'https://www.tradingview.com/symbols/{name_off.upper()}')
    if requests.get(f'https://www.tradingview.com/symbols/{name_off.upper()}').status_code != 404:
        await call.message.edit_media(photo)
    else:
        await call.message.edit_media(
            InputMediaPhoto(InputFile('/root/investBot/app/bot /templates/stock_demo.jpg')))
    await call.message.edit_caption(f'{get_info(name_off)}\n'
                                    f'<b>Цена: {round(price * count, 2)} ({count}x)</b>\n'
                                    , reply_markup=create_kb_stock(
            name,
            name_off,
            price,
            count
        ), parse_mode='html')


async def client_handler_back_stock(call: types.CallbackQuery):
    photo = InputFile('/root/investBot/app/bot /templates/main_demo.jpg')
    await call.message.edit_media(InputMediaPhoto(photo))
    await call.message.edit_caption(caption='<b>Личный кабинет</b>', reply_markup=client_keyboard.kb_client,
                                    parse_mode='html')


def register_client_my_stocks_handler(dp: Dispatcher):
    dp.register_callback_query_handler(client_handler_see_stocks,
                                       client_keyboard.client_callback.filter(choose='stocks'),
                                       state='*')
    dp.register_callback_query_handler(inline_sell_switch,
                                       sell_callback.filter(action='sell_switch'), state='*')
    dp.register_callback_query_handler(client_handler_see_stocks,
                                       sell_callback.filter(action='+'),
                                       state='*')
    dp.register_callback_query_handler(client_handler_see_stocks,
                                       sell_callback.filter(action='-'),
                                       state='*')
    dp.register_callback_query_handler(client_handler_see_stocks,
                                       sell_callback.filter(action='left'),
                                       state='*')
    dp.register_callback_query_handler(client_handler_see_stocks,
                                       sell_callback.filter(action='right'),
                                       state='*')
    dp.register_callback_query_handler(client_handler_back_stock,
                                       sell_callback.filter(action='back'),
                                       state='*')
    dp.register_callback_query_handler(client_handler_sell_stocks,
                                       sell_callback.filter(action='sell'),
                                       state='*')

