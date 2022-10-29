from aiogram.dispatcher.filters.state import State, StatesGroup


class Profile(StatesGroup):
    profile = State()
    photo_change = State()
    status = State()


class SetProfile(StatesGroup):
    name = State()
    surname = State()
    status = State()
    photo = State()


class Game(StatesGroup):
    game = State()
