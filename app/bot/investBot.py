from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from handlers import entrance, admin, inline
from handlers.client import client, client_profile, client_market, client_top, client_my_stocks
from create_bot import bot, storage


dp = Dispatcher(bot, storage=storage)

entrance.register_entrance_handler(dp)
client.register_client_handler(dp)
client_profile.register_client_profile_handler(dp)
client_market.register_client_market_handler(dp)
client_top.register_client_top_handler(dp)
client_my_stocks.register_client_my_stocks_handler(dp)
admin.register_admin_handler(dp)
inline.register_inline_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, timeout=5, loop=True)
