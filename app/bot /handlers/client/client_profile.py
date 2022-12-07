from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InputFile, InputMediaPhoto, ReplyKeyboardRemove
from keyboards.client_keyboards import client_keyboard, client_profile_keyboard, profile_back_keyboard
from keyboards.client_keyboards.client_profile_keyboard import new_callback
from create_bot import bot
from handlers.client.get_price import get_price
import requests


class Profile(StatesGroup):
    name = State()
    surname = State()
    photo_change = State()


async def client_handler_profile(call: types.CallbackQuery):
    t_id = {'tg_id': call.from_user.id}
    data = dict(requests.get('http://217.18.60.9/profile', json=t_id).json())
    account = float(data['account'].replace(',', '.'))
    account_brokerage = account
    for stock in requests.get('http://217.18.60.9/stocks', json={'tg_id': call.from_user.id}).json():
        try:
            price = float(stock['price'])
        except:
            price = 0
        try:
            account_brokerage += round(price * stock['count'], 2)
        except:
            pass
    if data['photo'] == 'default':
        photo = InputFile('/root/investBot/app/bot /templates/investor_demo.png')
    else:
        photo = data['photo']
    await call.message.edit_media(InputMediaPhoto(photo))
    await call.message.edit_caption(parse_mode='html', caption=f'<b>{data["name"]} {data["surname"]}</b>\nДенег на счету: <b>{round(account, 2)}$</b>\nДенег в портфеле: <b>{round(account_brokerage, 2)}$ ({-round(((1000-round(account_brokerage, 2))/1000)*100, 2)} %)</b>', reply_markup=client_profile_keyboard.kb_client_profile)


async def client_handler_profile_1(call: types.CallbackQuery):
    await call.message.answer("Имя:", reply_markup=profile_back_keyboard.kb_profile_back)
    await Profile.name.set()


async def client_handler_profile_name(message: types.message, state: FSMContext):
    name = {'tg_id': message.from_user.id, 'name': message.text}
    requests.put('http://217.18.60.9/profile', json=name)
    t_id = {'tg_id': message.from_user.id}
    data = requests.get('http://217.18.60.9/profile', json=t_id).json()
    if data['photo'] == 'default':
        photo = InputFile('/root/investBot/app/bot /templates/investor_demo.png')
    else:
        photo = data['photo']
    await message.answer('👈', reply_markup=ReplyKeyboardRemove())
    account = float(data['account'].replace(',', '.'))
    account_brokerage = account
    for stock in requests.get('http://217.18.60.9/stocks', json={'tg_id': message.from_user.id}).json():
        try:
            price = float(stock['price'])
        except:
            price = 0
        try:
            account_brokerage += round(price * stock['count'], 2)
        except:
            pass
    await bot.send_photo(message.from_user.id, photo,
                         f'<b>{data["name"]} {data["surname"]}</b>\nДенег на счету: <b>{round(account, 2)}$</b>\nДенег в портфеле: <b>{round(account_brokerage, 2)}$ ({-round(((1000 - round(account_brokerage, 2)) / 1000) * 100, 2)} %)</b>',
                        parse_mode='html',
                         reply_markup=client_profile_keyboard.kb_client_profile)
    await state.finish()


async def client_handler_profile_2(call: types.CallbackQuery):
    await Profile.surname.set()
    await call.message.answer('Отправьте фамилию', reply_markup=profile_back_keyboard.kb_profile_back)


async def client_handler_profile_surname(message: types.message, state: FSMContext):
    surname = {'tg_id': message.from_user.id, 'surname': message.text}
    requests.put('http://217.18.60.9/profile', json=surname)
    t_id = {'tg_id': message.from_user.id}
    data = requests.get('http://217.18.60.9/profile', json=t_id).json()
    if data['photo'] == 'default':
        photo = InputFile('/root/investBot/app/bot /templates/investor_demo.png')
    else:
        photo = data['photo']
    await message.answer('👈', reply_markup=ReplyKeyboardRemove())
    account = float(data['account'].replace(',', '.'))
    account_brokerage = account
    for stock in requests.get('http://217.18.60.9/stocks', json={'tg_id': message.from_user.id}).json():
        try:
            price = float(stock['price'])
        except:
            price = 0
        try:
            account_brokerage += round(price * stock['count'], 2)
        except:
            pass
    await bot.send_photo(message.from_user.id, photo,
                         f'<b>{data["name"]} {data["surname"]}</b>\nДенег на счету: <b>{round(account, 2)}$</b>\nДенег в портфеле: <b>{round(account_brokerage, 2)}$ ({-round(((1000 - round(account_brokerage, 2)) / 1000) * 100, 2)} %)</b>',
                         reply_markup=client_profile_keyboard.kb_client_profile, parse_mode='html')
    await state.finish()


async def client_handler_profile_3(call: types.CallbackQuery):
    await call.message.answer('Отправьте фотографию ', reply_markup=profile_back_keyboard.kb_profile_back)
    await Profile.photo_change.set()


async def client_handler_profile_photo(message: types.message, state: FSMContext):
    photo = {'photo': message.photo[0].file_id, 'tg_id': message.from_user.id}
    requests.put('http://217.18.60.9/profile', json=photo)
    t_id = {'tg_id': message.from_user.id}
    data = requests.get('http://217.18.60.9/profile', json=t_id).json()
    if data['photo'] == 'default':
        photo = InputFile('/root/investBot/app/bot /templates/investor_demo.png')
    else:
        photo = data['photo']
    await message.answer('👈', reply_markup=ReplyKeyboardRemove())
    account = float(data['account'].replace(',', '.'))
    account_brokerage = account
    for stock in requests.get('http://217.18.60.9/stocks', json={'tg_id': message.from_user.id}).json():
        try:
            price = float(stock['price'])
        except:
            price = 0
        try:
            account_brokerage += round(price * stock['count'], 2)
        except:
            pass
    await bot.send_photo(message.from_user.id, photo,
                         f'<b>{data["name"]} {data["surname"]}</b>\nДенег на счету: <b>{round(account, 2)}$</b>\nДенег в портфеле: <b>{round(account_brokerage, 2)}$ ({-round(((1000 - round(account_brokerage, 2)) / 1000) * 100, 2)} %)</b>',
                         reply_markup=client_profile_keyboard.kb_client_profile, parse_mode='html'),
    await state.finish()


async def client_handler_profile_4(call: types.CallbackQuery):
    photo = InputFile('/root/investBot/app/bot /templates/main_demo.jpg')
    await call.message.edit_media(InputMediaPhoto(photo))
    await call.message.edit_caption(caption='<b>Личный кабинет</b>', reply_markup=client_keyboard.kb_client, parse_mode='html')


async def client_handler_profile_back(message: types.message, state: FSMContext):
    await message.answer('👈', reply_markup=ReplyKeyboardRemove())
    t_id = {'tg_id': message.chat.id}
    data = dict(requests.get('http://217.18.60.9/profile', json=t_id).json())
    account = float(data['account'].replace(',', '.'))
    account_brokerage = account
    for stock in requests.get('http://217.18.60.9/stocks', json={'tg_id': message.from_user.id}).json():
        try:
            price = float(stock['price'])
        except:
            price = 0
        try:
            account_brokerage += round(price * stock['count'], 2)
        except:
            pass
    if data['photo'] == 'default':
        photo = InputFile('/root/investBot/app/bot /templates/investor_demo.png')
    else:
        photo = data['photo']
    await bot.send_photo(message.chat.id, photo,
                         f'<b>{data["name"]} {data["surname"]}</b>\nДенег на счету: <b>{round(account, 2)}$</b>\nДенег в портфеле: <b>{round(account_brokerage, 2)}$ ({-round(((1000 - round(account_brokerage, 2)) / 1000) * 100, 2)} %)</b>',
                         reply_markup=client_profile_keyboard.kb_client_profile,
                         parse_mode='html')
    await state.finish()


def register_client_profile_handler(dp: Dispatcher):
    dp.register_callback_query_handler(client_handler_profile, client_keyboard.client_callback.filter(choose='me'),
                                       state='*')
    dp.register_message_handler(client_handler_profile_back, Text(equals='Вернуться назад'), state='*')
    dp.register_callback_query_handler(client_handler_profile_1, new_callback.filter(digit='1'))
    dp.register_message_handler(client_handler_profile_name, state=Profile.name)
    dp.register_callback_query_handler(client_handler_profile_2, new_callback.filter(digit='2'))
    dp.register_message_handler(client_handler_profile_surname, state=Profile.surname)
    dp.register_callback_query_handler(client_handler_profile_3, new_callback.filter(digit='3'))
    dp.register_message_handler(client_handler_profile_photo, state=Profile.photo_change,
                                content_types=['photo'])
    dp.register_callback_query_handler(client_handler_profile_4, new_callback.filter(digit='4'),
                                       state='*')






