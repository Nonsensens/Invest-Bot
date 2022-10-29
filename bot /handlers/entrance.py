from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import start_keyboard
from keyboards.client_keyboards import client_keyboard
import requests


class RegEntrance(StatesGroup):
    username = State()
    password = State()
    name = State()
    surname = State()
    status = State()
    photo = State()


class LogEntrance(StatesGroup):
    username = State()
    password = State()


class User(StatesGroup):
    user = State()


async def register_handler_entrance(message: types.message):
    await message.answer("Привет! Я инвестиционный бот. Добро пожаловать🤓", reply_markup=start_keyboard.kb_start)
    t_id = {'tg_id': message.from_user.id}
    code = requests.get('http://127.0.0.1:5050/profile', json=t_id).status_code
    if code != 404:
        await message.answer('Аккаунт уже есть')
        return
    await RegEntrance.username.set()
    await message.answer('Процесс регистрации начат!✅\nВведите ваш никнейм:', reply_markup=types.ReplyKeyboardRemove())


async def register_handler_username(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text
    await RegEntrance.next()
    await message.answer("Введите ваш пароль:")


async def register_handler_password(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text
    await RegEntrance.next()
    await message.answer("Введите ваше имя:")


async def register_handler_name(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await RegEntrance.next()
    await message.answer("Введите вашу фамилию:")


async def register_handler_surname(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['surname'] = message.text
    await RegEntrance.next()
    await message.answer("Введите статус:")


async def register_handler_status(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['status'] = message.text
    await RegEntrance.next()
    await message.answer("Отправьте вашу фотографию")


async def register_handler_photo(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        username = data['username']
        password = data['password']
        name = data['name']
        surname = data['surname']
        status = data['status']
        photo = data['photo']
        tg_id = message.from_user.id
    data = {'username': username,
            'password': password,
            'name': name, 'surname': surname,
            'status': status,
            'photo': photo,
            'tg_id': tg_id,
            }
    await state.finish()
    if requests.post('http://127.0.0.1:5050/registration', json=data).status_code == 201:
        await User.user.set()
        await message.answer(f'Успешная регистрация, {username}💥', reply_markup=client_keyboard.kb_client)
    else:
        await message.answer('Что-то пошло не так', reply_markup=start_keyboard.kb_start)


async def login_handler_entrance(message: types.message):
    await LogEntrance.username.set()
    await message.answer('Процесс входа начат!✅\nВведите ваш никнейм:', reply_markup=types.ReplyKeyboardRemove())


async def login_handler_username(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text
    await LogEntrance.next()
    await message.answer('Введите ваш пароль:')


async def login_handler_password(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text
        username = data['username']
        password = data['password']
    data = {'username': username, 'password': password}
    await state.finish()
    if requests.post('http://127.0.0.1:5050/login', json=data).status_code == 201:
        await message.answer('Успешный вход🌕', reply_markup=client_keyboard.kb_client)
        await User.user.set()
    else:
        await message.answer('Что-то пошло не так', reply_markup=start_keyboard.kb_start)


def register_entrance_handler(dp: Dispatcher):
    dp.register_message_handler(register_handler_entrance, commands='start', state=None)
    dp.register_message_handler(register_handler_username, state=RegEntrance.username)
    dp.register_message_handler(register_handler_password, state=RegEntrance.password)
    dp.register_message_handler(register_handler_name, state=RegEntrance.name)
    dp.register_message_handler(register_handler_surname, state=RegEntrance.surname)
    dp.register_message_handler(register_handler_status, state=RegEntrance.status)
    dp.register_message_handler(register_handler_photo, state=RegEntrance.photo, content_types=['photo'])
    dp.register_message_handler(login_handler_entrance, commands='Войти', commands_prefix='💎', state=None)
    dp.register_message_handler(login_handler_username, state=LogEntrance.username)
    dp.register_message_handler(login_handler_password, state=LogEntrance.password)


