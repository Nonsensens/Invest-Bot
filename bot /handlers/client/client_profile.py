from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from handlers.entrance import User
from handlers.client import models_client
from keyboards.client_keyboards import client_keyboard, client_profile_keyboard, profile_back_keyboard
from aiogram.dispatcher import FSMContext
from create_bot import bot
import requests


async def client_handler_profile_1(message: types.message):
    await message.answer("Имя:", reply_markup=profile_back_keyboard.kb_profile_back)
    await models_client.SetProfile.name.set()


async def client_handler_profile_name(message: types.message, state: FSMContext):
    if message.text == 'Вернуться назад':
        t_id = {'tg_id': message.from_user.id}
        data = requests.get('http://127.0.0.1:5050/profile', json=t_id).json()
        await bot.send_photo(message.from_user.id, data["photo"],
                             f'\n{data["name"]} {data["surname"]} - {data["status"]}\nДенег на счету: {data["account"]}',
                             reply_markup=client_profile_keyboard.kb_client_profile)
        await message.answer('1. Заполнить профиль заново\n2. Изменить фото\n3. Изменить статус профиля\n4. Назад')
        await models_client.Profile.profile.set()
        return
    async with state.proxy() as data:
        data['name'] = message.text
    await models_client.SetProfile.next()
    await message.answer("Фамилия:")


async def client_handler_profile_surname(message: types.message, state: FSMContext):
    if message.text == 'Вернуться назад':
        t_id = {'tg_id': message.from_user.id}
        data = requests.get('http://127.0.0.1:5050/profile', json=t_id).json()
        await bot.send_photo(message.from_user.id, data["photo"],
                             f'\n{data["name"]} {data["surname"]} - {data["status"]}\nДенег на счету: {data["account"]}',
                             reply_markup=client_profile_keyboard.kb_client_profile)
        await message.answer('1. Заполнить профиль заново\n2. Изменить фото\n3. Изменить статус профиля\n4. Назад')
        await models_client.Profile.profile.set()
        return
    async with state.proxy() as data:
        data['surname'] = message.text
    await models_client.SetProfile.next()
    await message.answer("Cтатус:")


async def client_handler_status(message: types.message, state: FSMContext):
    if message.text == 'Вернуться назад':
        t_id = {'tg_id': message.from_user.id}
        data = requests.get('http://127.0.0.1:5050/profile', json=t_id).json()
        await bot.send_photo(message.from_user.id, data["photo"],
                             f'\n{data["name"]} {data["surname"]} - {data["status"]}\nДенег на счету: {data["account"]}',
                             reply_markup=client_profile_keyboard.kb_client_profile)
        await message.answer('1. Заполнить профиль заново\n2. Изменить фото\n3. Изменить статус профиля\n4. Назад')
        await models_client.Profile.profile.set()
        return
    async with state.proxy() as data:
        data['status'] = message.text
    await models_client.SetProfile.next()
    await message.answer("Фото:")


async def client_handler_photo(message: types.message, state: FSMContext):
    if message.text == 'Вернуться назад':
        t_id = {'tg_id': message.from_user.id}
        data = requests.get('http://127.0.0.1:5050/profile', json=t_id).json()
        await bot.send_photo(message.from_user.id, data["photo"],
                             f'\n{data["name"]} {data["surname"]} - {data["status"]}\nДенег на счету: {data["account"]}',
                             reply_markup=client_profile_keyboard.kb_client_profile)
        await message.answer('1. Заполнить профиль заново\n2. Изменить фото\n3. Изменить статус профиля\n4. Назад')
        await models_client.Profile.profile.set()
        return
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        name = data['name']
        surname = data['surname']
        status = data['status']
        photo = data['photo']
        tg_id = message.from_user.id
    data = {'name': name, 'surname': surname,
            'status': status,
            'photo': photo,
            'tg_id': tg_id,
            }
    await state.finish()
    requests.put('http://127.0.0.1:5050/profile', json=data)
    t_id = {'tg_id': message.from_user.id}
    data = requests.get('http://127.0.0.1:5050/profile', json=t_id).json()
    await bot.send_photo(message.from_user.id, data["photo"],
                         f'\n{data["name"]} {data["surname"]} - {data["status"]}\nДенег на счету: {data["account"]}',
                         reply_markup=client_profile_keyboard.kb_client_profile)
    await message.answer('1. Заполнить профиль заново\n2. Изменить фото\n3. Изменить статус профиля\n4. Назад')
    await models_client.Profile.profile.set()


async def client_handler_profile_2(message: types.message):
    if message.text == '2':
        await message.answer('Отправьте фотографию ', reply_markup=profile_back_keyboard.kb_profile_back)
        await models_client.Profile.photo_change.set()


async def client_handler_profile_photo(message: types.message):
    photo = {'photo': message.photo[0].file_id, 'tg_id': message.from_user.id}
    requests.put('http://127.0.0.1:5050/profile', json=photo)
    t_id = {'tg_id': message.from_user.id}
    data = requests.get('http://127.0.0.1:5050/profile', json=t_id).json()
    await bot.send_photo(message.from_user.id, data["photo"],
                         f'\n{data["name"]} {data["surname"]} - {data["status"]}\nДенег на счету: {data["account"]}',
                         reply_markup=client_profile_keyboard.kb_client_profile)
    await message.answer('1. Заполнить профиль заново\n2. Изменить фото\n3. Изменить статус профиля\n4. Назад')
    await models_client.Profile.profile.set()


async def client_handler_profile_3(message: types.message):
    await models_client.Profile.status.set()
    await message.answer('Отправьте статус', reply_markup=profile_back_keyboard.kb_profile_back)


async def client_handler_profile_status(message: types.message):
    if message.text == 'Вернуться назад':
        t_id = {'tg_id': message.from_user.id}
        data = requests.get('http://127.0.0.1:5050/profile', json=t_id).json()
        await bot.send_photo(message.from_user.id, data["photo"],
                             f'\n{data["name"]} {data["surname"]} - {data["status"]}\nДенег на счету: {data["account"]}',
                             reply_markup=client_profile_keyboard.kb_client_profile)
        await message.answer('1. Заполнить профиль заново\n2. Изменить фото\n3. Изменить статус профиля\n4. Назад')
        await models_client.Profile.profile.set()
        return
    status = {'tg_id': message.from_user.id, 'status': message.text}
    requests.put('http://127.0.0.1:5050/profile', json=status)
    t_id = {'tg_id': message.from_user.id}
    data = requests.get('http://127.0.0.1:5050/profile', json=t_id).json()
    await bot.send_photo(message.from_user.id, data["photo"],
                         f'\n{data["name"]} {data["surname"]} - {data["status"]}\nДенег на счету: {data["account"]}',
                         reply_markup=client_profile_keyboard.kb_client_profile)
    await message.answer('1. Заполнить профиль заново\n2. Изменить фото\n3. Изменить статус профиля\n4. Назад')
    await models_client.Profile.profile.set()


async def client_handler_profile_4(message: types.message):
    await message.answer('👈', reply_markup=client_keyboard.kb_client)
    await User.user.set()


async def client_handler_profile_back(message: types.message):
    t_id = {'tg_id': message.from_user.id}
    data = requests.get('http://127.0.0.1:5050/profile', json=t_id).json()
    await bot.send_photo(message.from_user.id, data["photo"],
                         f'\n{data["name"]} {data["surname"]} - {data["status"]}\nДенег на счету: {data["account"]}',
                         reply_markup=client_profile_keyboard.kb_client_profile)
    await message.answer('1. Заполнить профиль заново\n2. Изменить фото\n3. Изменить статус профиля\n4. Назад')
    await models_client.Profile.profile.set()


def register_client_profile_handler(dp: Dispatcher):
    dp.register_message_handler(client_handler_profile_1, Text(equals='1'), state=models_client.Profile.profile)
    dp.register_message_handler(client_handler_profile_name, state=models_client.SetProfile.name)
    dp.register_message_handler(client_handler_profile_surname, state=models_client.SetProfile.surname)
    dp.register_message_handler(client_handler_status, state=models_client.SetProfile.status)
    dp.register_message_handler(client_handler_photo, state=models_client.SetProfile.photo, content_types=['photo'])
    dp.register_message_handler(client_handler_profile_2, Text(equals='2'), state=models_client.Profile.profile)
    dp.register_message_handler(client_handler_profile_photo, state=models_client.Profile.photo_change, content_types=['photo'])
    dp.register_message_handler(client_handler_profile_3, Text(equals='3'), state=models_client.Profile.profile)
    dp.register_message_handler(client_handler_profile_status, state=models_client.Profile.status)
    dp.register_message_handler(client_handler_profile_4, Text(equals='4'), state=models_client.Profile.profile)
    dp.register_message_handler(client_handler_profile_back, Text(equals='Вернуться назад'), state='*')




