import hashlib
import requests
from aiogram.types import InputFile, InputMediaPhoto
from bs4 import BeautifulSoup as bs
from keyboards.stock_keyboard import create_kb_stock_switch, create_kb_stock, buy_callback
from keyboards.client_keyboards.client_keyboard import kb_client
from aiogram import Dispatcher, types
from create_bot import bot


def get_info(symbol):
    r = requests.get(f'https://www.tinkoff.ru/invest/stocks/{symbol}/')
    html = bs(r.content, 'html.parser')
    about = html.find('h1', {'class': "SecurityBlockHeader__title_KUEiP"}).text
    about_sub = html.find('div', {'data-qa-file': "SecurityInfo"}).text
    about_sub = about_sub.split('.')
    about_sub.pop(-1)
    about_sub = '.'.join(about_sub)
    str = '<b>' + about + '</b>' + '\n' + about_sub
    return str


def get_query(q):
    session = requests.Session()
    req = session.get(f'https://www.tinkoff.ru/invest/recommendations/?query={q}').content
    stocks = list()
    html = bs(req, 'html.parser')
    names = [item.text for item in html.find_all("div", class_="SecurityRow__showName_inlal")]
    names_off = [item.text for item in html.find_all("div", class_="SecurityRow__ticker_KMm7A")]
    imgs = [f"https:{item['src']}" for item in html.find_all("img", class_="InvestLogo__image_rmSHy")]
    prices = [item.text.replace('\xa0', '') for item in html.find_all("span", class_="Money-module__money_UZBbh") if item.text.replace('\xa0', '')[0] != '+' and item.text.replace('\xa0', '')[0] != '−' and item.text.replace('\xa0', '')[0] != '0']
    k = 0
    while k != len(names):
        try:
            stock = {'name': names[k], 'name_off': names_off[k], 'img': imgs[k], 'price': prices[k]}
            stocks.append(stock)
        except:
            pass
        k += 1
    return stocks


async def inline_search(query: types.InlineQuery):
    text = query.query or ''
    stocks = get_query(text)[:11]
    articles = [types.InlineQueryResultArticle(
        id=hashlib.md5(stock['name_off'].encode()).hexdigest(),
        thumb_url=stock['img'],
        title=stock['name'],
        description=stock['name_off'],
        input_message_content=types.InputTextMessageContent(message_text=
                                                            f'{stock["name"]}\n'
                                                            f'Цена: {stock["price"]}\n'
                                                            ,),
        reply_markup=create_kb_stock_switch(
            stock['name'][:10],
            stock['name_off'][:10],
            stock['price'][:len(stock['price'])-1],
            '1'),
    ) for stock in stocks]
    await query.answer(articles, cache_time=60)


async def inline_buy_switch(call: types.CallbackQuery):
    data = call.data.split('~')
    name = data[1]
    name_off = data[2]
    price = float(str(data[3]).replace(',', '.'))
    count = 1
    try:
        photo = f'https://www.tradingview.com/symbols/{name_off.upper()}'
        if requests.get(f'https://www.tradingview.com/symbols/{name_off.upper()}').status_code != 404:
            pass
        else:
                photo = InputFile('/root/investBot/app/bot /templates/stock_demo.jpg')
        await bot.send_photo(call.from_user.id, photo=photo, caption=f'{get_info(name_off)}\n'
                                                                     f'<b>Цена: {round(price * count, 2)} ({count}x)</b>\n'
                             , reply_markup=create_kb_stock(
                name,
                name_off,
                price,
                count
            ), parse_mode='html')

    except:
        return


async def inline_buy(call: types.CallbackQuery):
    data = call.data.split('~')
    name = data[1]
    name_off = data[2]
    price = float(str(data[3]).replace(',', '.'))
    count_buy = int(data[4])
    t_id = {'tg_id': call.from_user.id}
    data = dict(requests.get('http://217.18.60.9/profile', json=t_id).json())
    account = float(data['account'].replace(',', '.'))
    if round(account - price * count_buy, 2) >= 0:
        requests.put('http://217.18.60.9/profile',
                     json={'tg_id': call.from_user.id, 'account': str(round(account - round(price*count_buy, 2), 2))})
        try:
            count = int(requests.post('http://217.18.60.9/stocks',
                                      json={'tg_id': call.from_user.id, 'name_off': name_off}).json()['count'])
        except:
            count = 0
        if count >= 1:
            requests.put('http://217.18.60.9/stocks',
                         json={'tg_id': call.from_user.id, 'name_off': name_off, 'count': count + count_buy})
            if count_buy != 1:
                await call.message.edit_caption(f'{get_info(name_off)}\n'
                                                f'<b>Цена: {round(price, 2)} ({1}x)</b>\n', reply_markup=create_kb_stock(
                    name,
                    name_off,
                    price,
                    1
                ),parse_mode="html")
            await call.answer('Успешная покупка')
        else:
            resp = requests.post('http://217.18.60.9/addstock', json={
                'name': name,
                'name_off': name_off,
                'price': price,
                'price_old': price,
                'tg_id': call.from_user.id,
                'count': count_buy
            })
            if resp.status_code == 205:
                await call.answer('Успешная покупка!')
                if count_buy != 1:
                    await call.message.edit_caption(f'{get_info(name_off)}\n'
                                                                                                                             f'Цена: {round(price*1, 2)} ({1}x)\n', reply_markup=create_kb_stock(
                name,
                name_off,
                price,
                1
            ))
            else:
                await call.answer('Что-то пошло не так')
    else:
        await call.answer('Недостаточно средств')


async def inline_change(call: types.CallbackQuery):
    data = call.data.split('~')
    name = data[1]
    price = float(data[3])
    count = int(data[4])
    if data[5] == '+':
        await call.message.edit_caption(f'{get_info(data[2])}\n'
                                                                                                                         f'<b>Цена: {round(price*(count+1), 2)} ({count+1}x)</b>\n', parse_mode='html', reply_markup=create_kb_stock(
            name,
            data[2],
            price,
            count+1
        ))
    else:
        if count - 1 == 0:
            await call.answer('Нельзя')
            return
        await call.message.edit_caption(f'{get_info(data[2])}\n'
                                        f'<b>Цена: {round(price * (count - 1), 2)} ({count - 1}x)</b>\n',
                                        parse_mode='html',
                                        reply_markup=create_kb_stock(
                                            name,
                                            data[2],
                                            price,
                                            count - 1
                                        )
                                        )


async def inline_back_to_cab(call: types.CallbackQuery):
    photo = InputFile('/root/investBot/app/bot /templates/main_demo.jpg')
    await call.message.edit_media(InputMediaPhoto(photo))
    await call.message.edit_caption(caption='<b>Личный кабинет</b>', reply_markup=kb_client,
                                    parse_mode='html')


def register_inline_handlers(dp:Dispatcher):
    dp.register_inline_handler(inline_search, state='*')
    dp.register_callback_query_handler(inline_change, buy_callback.filter(action='+'), state='*')
    dp.register_callback_query_handler(inline_change, buy_callback.filter(action='-'), state='*')
    dp.register_callback_query_handler(inline_buy_switch, buy_callback.filter(action='buy_switch'), state='*')
    dp.register_callback_query_handler(inline_buy, buy_callback.filter(action='buy'), state='*')
    dp.register_callback_query_handler(inline_back_to_cab, buy_callback.filter(action='cabinet'), state='*')
