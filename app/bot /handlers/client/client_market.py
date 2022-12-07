import requests
from create_bot import bot
from bs4 import BeautifulSoup as bs
from handlers.client.get_price import get_price
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InputFile, InputMediaPhoto
from keyboards.client_keyboards import client_keyboard
from keyboards import market_keyboard, market_switch_keyboard, market_news_keyboard, market_suggestions_keyboard


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
    except:
        str = '<b>' + symbol + '</b>'
    return str


def get_query(q):
    session = requests.Session()
    req = session.get(f'https://www.tinkoff.ru/invest/recommendations/?query={q}').content
    stocks = list()
    html = bs(req, 'html.parser')
    names = [item.text for item in html.find_all("div", class_="SecurityRow__showName_inlal")]
    names_off = [item.text for item in html.find_all("div", class_="SecurityRow__ticker_KMm7A")]
    imgs = [f"https:{item['src']}" for item in html.find_all("img", class_="InvestLogo__image_rmSHy")]
    k = 0
    while k != len(names):
        try:
            stock = {'name': names[k], 'name_off': names_off[k], 'img': imgs[k], 'price': 0}
            stocks.append(stock)
        except:
            pass
        k += 1
    return stocks


class Searcher(StatesGroup):
    search = State()


async def client_handler_market(call: types.CallbackQuery, state: FSMContext):
    photo = InputFile('/root/investBot/app/bot /templates/market_demo.jpg')
    await call.message.edit_media(InputMediaPhoto(photo))
    await call.message.edit_caption('<b>Фондовый рынок</b>', parse_mode='html', reply_markup=market_keyboard.kb_market)
    await state.finish()


async def client_handler_market_search(call: types.CallbackQuery):
    await call.message.answer('Введите название')
    await Searcher.search.set()


async def client_handler_market_find_message(message: types.Message):
    query = message.text
    cur = 0
    count = 1
    stocks = get_query(query)
    if not stocks:
        await message.answer('Ничего не найдено')
        await message.answer('Введите название')
        await Searcher.search.set()
        return
    stock = stocks[cur]
    name_off = stock['name_off']
    price = get_price(name_off)
    photo = f'https://www.tradingview.com/symbols/{name_off.upper()}'
    if requests.get(f'https://www.tradingview.com/symbols/{name_off.upper()}').status_code != 404:
        pass
    else:
        photo = InputFile('/root/investBot/app/bot /templates/stock_demo.jpg')
    await bot.send_photo(message.from_user.id, photo=photo, caption=f'{get_info(stock["name_off"])[:1000]}\n'
                                    f'<b>Цена: {round(price  * count, 2)}$ ({count}x)</b>\n'
                                   , reply_markup=market_switch_keyboard.create_kb_market_switch(
            cur=cur,
            q=query,
            count=count
        ), parse_mode='html')


async def client_handler_market_find_call(call: types.CallbackQuery):
    data = call.data.split('~')
    cur = int(data[2])
    query = data[3]
    count = int(data[1])
    action = data[-1]
    stocks = get_query(query)
    if not stocks:
        await call.message.answer('Ничего не найдено')
        await call.message.answer('Введите название')
        await Searcher.search.set()
        return
    if action == 'left' or action == 'right':
        if action == 'left':
            cur -= 1
        else:
            cur += 1
        if cur > len(stocks) - 1:
            cur = 0
        elif cur < 0:
            cur = len(stocks) - 1
    if action == '-':
        count -= 1
    if action == '+':
        count += 1
    if count < 1:
        await call.answer('Нельзя')
        return
    stock = stocks[cur]
    name_off = stock['name_off']
    price = get_price(name_off)
    photo = InputMediaPhoto(f'https://www.tradingview.com/symbols/{name_off.upper()}')
    if requests.get(f'https://www.tradingview.com/symbols/{name_off.upper()}').status_code != 404:
        pass
    else:
        photo = InputMediaPhoto(InputFile('/root/investBot/app/bot /templates/stock_demo.jpg'))
    await call.message.edit_media(photo)
    await call.message.edit_caption(f'{get_info(stock["name_off"])[:1000]}\n'
                                    f'<b>Цена: {round(price  * count, 2)}$ ({count}x)</b>\n'
                                   , reply_markup=market_switch_keyboard.create_kb_market_switch(
            cur=cur,
            q=query,
            count=count
        ), parse_mode='html')


async def client_handler_market_buy(call: types.CallbackQuery):
    data = call.data.split('~')
    if data[-1] == 'buy_sug':
        cur = int(data[2])
        html = bs(
            requests.get(
                'https://www.ii.co.uk/investing-with-ii/international-investing/most-popular-us-stocks').content,
            'lxml')
        stocks = [stock.text for stock in html.find_all('td')]
        stocks = stocks[3:53]
        while '' in stocks:
            stocks.remove('')
        name = stocks[cur]
        name_off = stocks[cur+1]
        price = get_price(name_off)
    else:
        cur = int(data[2])
        query = data[3]
        stocks = get_query(query)
        stock = stocks[cur]
        name_off = stock['name_off']
        price = get_price(name_off)
        name = stock['name']
    count_buy = int(data[1])
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
            else:
                await call.answer('Что-то пошло не так')
    else:
        await call.answer('Недостаточно средств')


async def client_handler_market_news(call: types.CallbackQuery):
    data = call.data.split('~')
    html = bs(requests.get('https://quote.rbc.ru/tag/stocks').content, 'html.parser')
    news = [(' ').join(new.text.split()) for new in html.find_all('span', {'class': 'q-item__title'})]
    imgs = [new['src'] for new in html.find_all('img', {'alt': 'Фото: Shutterstock'})]
    if len(data) > 2:
        cur = int(data[1])
        if data[2] == 'left' and cur - 1 >= 0:
            cur -= 1
        if data[2] == 'right' and cur + 1 < len(news) - 1:
            cur += 1
        await call.message.edit_media(InputMediaPhoto(imgs[cur]))
        await call.message.edit_caption(f'<b>{news[cur]}</b>', reply_markup=market_news_keyboard.create_kb_market_news(cur), parse_mode='html')
    else:
        await call.message.edit_media(InputMediaPhoto(imgs[0]))
        await call.message.edit_caption(f'<b>{news[0]}</b>',
                                        reply_markup=market_news_keyboard.create_kb_market_news(0), parse_mode='html')


async def client_handler_market_suggestions(call: types.CallbackQuery):
    data = call.data.split('~')
    html = bs(
        requests.get('https://www.ii.co.uk/investing-with-ii/international-investing/most-popular-us-stocks').content,
        'lxml')
    stocks = [stock.text for stock in html.find_all('td')]
    stocks = stocks[3:53]
    while '' in stocks:
        stocks.remove('')
    if len(data) > 2:
        count = int(data[1])
        action = data[-1]
        if action == '-':
            count -= 1
        if action == '+':
            count += 1
        if count < 1:
            await call.answer('Нельзя')
            return
        cur = int(data[2])
        if data[-1] == 'left' and cur - 1 >=0:
            cur -= 2
        elif data[-1] == 'left' and cur - 1 < 0:
            cur = len(stocks) - 2
        if data[-1] == 'right' and cur + 1 < len(stocks) - 1:
            cur += 2
        elif data[-1] == 'right' and cur + 1 >= len(stocks) - 1:
            cur = 0
        name_off = stocks[cur + 1]
        price = get_price(name_off)
        photo = InputMediaPhoto(f'https://www.tradingview.com/symbols/{name_off.upper()}')
        if requests.get(f'https://www.tradingview.com/symbols/{name_off.upper()}').status_code != 404:
            pass
        else:
            photo = InputMediaPhoto(InputFile('/root/investBot/app/bot /templates/stock_demo.jpg'))
        await call.message.edit_media(photo)
        await call.message.edit_caption(f'{get_info(name_off)}\n'
                                                                        f'<b>Цена: {round(price * count, 2)}$ ({count}x)</b>\n', reply_markup=market_suggestions_keyboard.create_kb_market_suggestions(
            cur=cur,
            count=count
        ), parse_mode='html')
    else:
        name_off = stocks[1]
        price = get_price(name_off)
        photo = InputMediaPhoto(f'https://www.tradingview.com/symbols/{name_off.upper()}')
        if requests.get(f'https://www.tradingview.com/symbols/{name_off.upper()}').status_code != 404:
            pass
        else:
            photo = InputMediaPhoto(
                InputFile('/root/investBot/app/bot /templates/stock_demo.jpg'))
        await call.message.edit_media(photo)
        await call.message.edit_caption(f'{get_info(name_off)}\n'
                                        f'<b>Цена: {round(price * 1, 2)}$ ({1}x)</b>\n',
                                        reply_markup=market_suggestions_keyboard.create_kb_market_suggestions(
                                            cur=0,
                                            count=1
                                        ), parse_mode='html')


async def client_handler_market_back(call: types.CallbackQuery):
    photo = InputFile('/root/investBot/app/bot /templates/main_demo.jpg')
    await call.message.edit_media(InputMediaPhoto(photo))
    await call.message.edit_caption(caption='<b>Личный кабинет</b>', reply_markup=client_keyboard.kb_client,
                                    parse_mode='html')


def register_client_market_handler(dp: Dispatcher):
    dp.register_callback_query_handler(client_handler_market_suggestions,
                                       market_keyboard.market_callback.filter(action='suggestions'),
                                       state='*')
    dp.register_callback_query_handler(client_handler_market_suggestions,
                                       market_suggestions_keyboard.kb_suggestions_callback.filter(action='left'),
                                       state='*')
    dp.register_callback_query_handler(client_handler_market_suggestions,
                                       market_suggestions_keyboard.kb_suggestions_callback.filter(action='right'),
                                       state='*')
    dp.register_callback_query_handler(client_handler_market_suggestions,
                                       market_suggestions_keyboard.kb_suggestions_callback.filter(action='-'),
                                       state='*')
    dp.register_callback_query_handler(client_handler_market_suggestions,
                                       market_suggestions_keyboard.kb_suggestions_callback.filter(action='+'),
                                       state='*')
    dp.register_callback_query_handler(client_handler_market_buy,
                                       market_suggestions_keyboard.kb_suggestions_callback.filter(action='buy_sug'),
                                       state='*')
    dp.register_callback_query_handler(client_handler_market,
                                       market_suggestions_keyboard.kb_suggestions_callback.filter(action='back'),
                                       state='*')
    dp.register_callback_query_handler(client_handler_market_news,
                                       market_keyboard.market_callback.filter(action='news'),
                                       state='*')
    dp.register_callback_query_handler(client_handler_market_news,
                                       market_news_keyboard.kb_news_callback.filter(action='left'),
                                       state='*')
    dp.register_callback_query_handler(client_handler_market_news,
                                       market_news_keyboard.kb_news_callback.filter(action='right'),
                                       state='*')
    dp.register_callback_query_handler(client_handler_market,
                                       market_news_keyboard.kb_news_callback.filter(action='back'),
                                       state='*')
    dp.register_callback_query_handler(client_handler_market, client_keyboard.client_callback.filter(choose='market'),
                                       state='*')
    dp.register_callback_query_handler(client_handler_market_search,
                                       market_keyboard.market_callback.filter(action='search'),
                                       state='*')
    dp.register_callback_query_handler(client_handler_market_back,
                                       market_keyboard.market_callback.filter(action='back'),
                                       state='*')
    dp.register_callback_query_handler(client_handler_market,
                                       market_switch_keyboard.switch_market_buy_callback.filter(action='back'),
                                       state='*')
    dp.register_message_handler(client_handler_market_find_message,
                                       state=Searcher.search,
                                       )
    dp.register_callback_query_handler(client_handler_market_find_call,
                                       market_switch_keyboard.switch_market_buy_callback.filter(action='right'),
                                       state='*')
    dp.register_callback_query_handler(client_handler_market_find_call,
                                       market_switch_keyboard.switch_market_buy_callback.filter(action='left'),
                                       state='*')
    dp.register_callback_query_handler(client_handler_market_find_call,
                                       market_switch_keyboard.switch_market_buy_callback.filter(action='+'),
                                       state='*')
    dp.register_callback_query_handler(client_handler_market_find_call,
                                       market_switch_keyboard.switch_market_buy_callback.filter(action='-'),
                                       state='*')
    dp.register_callback_query_handler(client_handler_market,
                                       market_switch_keyboard.switch_market_buy_callback.filter(action='back'),
                                       state='*')
    dp.register_callback_query_handler(client_handler_market_buy,
                                       market_switch_keyboard.switch_market_buy_callback.filter(action='buy_ser'),
                                       state='*')
    dp.register_callback_query_handler(client_handler_market_back, market_keyboard.market_callback.filter(action='back'),
                                       state='*')

