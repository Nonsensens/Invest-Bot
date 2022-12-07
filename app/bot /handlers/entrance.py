from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InputFile, ReplyKeyboardRemove
from keyboards.client_keyboards import client_keyboard
from keyboards.skip_photo_keyboard import kb_skip_photo
from create_bot import bot
import requests


class RegEntrance(StatesGroup):
    name = State()
    surname = State()
    photo = State()


async def register_handler_entrance(message: types.message):
    await message.answer("Привет! Я инвестиционный бот. Добро пожаловать🤓", reply_markup=ReplyKeyboardRemove())
    t_id = {'tg_id': message.from_user.id}
    code = requests.get('http://217.18.60.9/profile', json=t_id).status_code
    if code != 404:
        photo = InputFile('/root/investBot/app/bot /templates/main_demo.jpg')
        await bot.send_photo(message.from_user.id, photo, '<b>Личный кабинет</b>', parse_mode='html', reply_markup=client_keyboard.kb_client)
        return
    await RegEntrance.name.set()
    await message.answer('Процесс регистрации начат!✅\nВведите ваше имя:', reply_markup=types.ReplyKeyboardRemove())


async def register_handler_return(message: types.message):
   return


async def register_handler_name(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await RegEntrance.next()
    await message.answer("Введите вашу фамилию:")


async def register_handler_surname(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['surname'] = message.text
    await RegEntrance.next()
    await message.answer("Отправьте фото или пропустите:", reply_markup=kb_skip_photo)


async def register_handler_photo(message: types.message, state: FSMContext):
    if message.text == 'Пропустить':
        async with state.proxy() as data:
            name = data['name']
            surname = data['surname']
            tg_id = message.from_user.id
        data = {'name': name, 'surname': surname,
                'tg_id': tg_id,
                }
        await state.finish()
        if requests.post('http://217.18.60.9/registration', json=data).status_code == 201:
            await message.answer(f'Успешная регистрация, {name} {surname}💥', reply_markup=ReplyKeyboardRemove())
            photo = InputFile('/root/investBot/app/bot /templates/main_demo.jpg')
            await bot.send_photo(message.from_user.id, photo, '<b>Личный кабинет</b>', parse_mode='html', reply_markup=client_keyboard.kb_client)
            return
        else:
            await message.answer('Что-то пошло не так', reply_markup=ReplyKeyboardRemove())
            await state.finish()
            return
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        name = data['name']
        surname = data['surname']
        photo = data['photo']
        tg_id = message.from_user.id
    data = {'name': name, 'surname': surname,
            'photo': photo,
            'tg_id': tg_id,
            }
    await state.finish()
    if requests.post('http://217.18.60.9/registration', json=data).status_code == 201:
        await message.answer(f'Успешная регистрация, {name} {surname}💥', reply_markup=ReplyKeyboardRemove())
        photo = InputFile('/root/investBot/app/bot /templates/main_demo.jpg')
        await bot.send_photo(message.from_user.id, photo, '<b>Личный кабинет</b>', parse_mode='html', reply_markup=client_keyboard.kb_client)
    else:
        await message.answer('Что-то пошло не так', reply_markup=ReplyKeyboardRemove())


def register_entrance_handler(dp: Dispatcher):
    dp.register_message_handler(register_handler_entrance, commands='start', state=None)
    dp.register_message_handler(register_handler_return,  state=None)
    dp.register_message_handler(register_handler_name, state=RegEntrance.name)
    dp.register_message_handler(register_handler_surname, state=RegEntrance.surname)
    dp.register_message_handler(register_handler_photo, state=RegEntrance.photo, content_types=['photo'])
    dp.register_message_handler(register_handler_photo, state=RegEntrance.photo)


