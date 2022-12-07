import requests
from bs4 import BeautifulSoup as bs


def get_price(symbol):
    token = 'ce1189iad3i5s1t2f8s0ce1189iad3i5s1t2f8sg'
    url = f'https://finnhub.io/api/v1/quote?symbol={symbol.upper()}&token={token}'
    r = requests.get(url).json()
    price = r['c']
    if price == 0:
        try:
            html = bs(requests.get(f'https://www.tinkoff.ru/invest/stocks/{symbol}').content, 'html.parser')
            price = html.find('span', {'class': "Money-module__money_UZBbh"}).text
        except:
            pass
        try:
            html = bs(requests.get(f'https://www.tinkoff.ru/invest/etfs/{symbol}').content, 'html.parser')
            price = html.find('span', {'class': "Money-module__money_UZBbh"}).text
        except:
            pass
        try:
            html = bs(requests.get(f'https://www.tinkoff.ru/invest/bonds/{symbol}').content, 'html.parser')
            price = html.find('span', {'class': "Money-module__money_UZBbh"}).text
        except:
            pass
        try:
            html = bs(requests.get(f'https://www.tinkoff.ru/invest/futures/{symbol}').content, 'html.parser')
            price = html.find('span', {'class': "Money-module__money_UZBbh"}).text
        except:
            pass
        if len(price.split(',')) != 1:
            price = price.split(',')
            v = price[1][-1]
            price[0] = ''.join([i for i in price[0] if i.isdigit()])
            price[1] = ''.join([i for i in price[1] if i.isdigit()])
            price = float('.'.join(price))
            if v == '€':
                price = round(price / 1.04, 2)
            elif v == '₽':
                price = round(price / 61, 2)
            return price
        v = price[-1]
        price = float(''.join([i for i in price if i.isdigit()]))
        if v == '€':
            price = round(price / 1.04, 2)
        elif v == '₽':
            price = round(price / 61, 2)
        return price
    return r['c']


