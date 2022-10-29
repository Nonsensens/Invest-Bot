from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from handlers import entrance, admin
from handlers.client import client, client_profile, client_game
from create_bot import bot, storage


dp = Dispatcher(bot, storage=storage)

entrance.register_entrance_handler(dp)
client.register_client_handler(dp)
client_profile.register_client_profile_handler(dp)
client_game.register_client_game_handler(dp)
admin.register_admin_handler(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
