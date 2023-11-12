from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging
from aiogram.contrib.middlewares.logging import LoggingMiddleware


storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)

log_name = 'logs.log'
logging.basicConfig(
    filename=log_name,
    filemode='w',
    format='%(asctime)s.%(msecs)d %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO
)
dp.middleware.setup(LoggingMiddleware())


class States(StatesGroup):
    user_add = State()
    user_remove = State()
    user_update = State()
    admin_add = State()
    admin_remove = State()
    user_upd = State()
    photo_to_send = State()
    change_responsible = State()


# все элементы должны быть уникальными, иначе метод get_usr_meal в connection_db будет плохо работать
dinners_sets = [
    'Суп №1 🍜',
    'Суп №2 🍜',
    'Второе №1 🍱',
    'Второе №2 🍱',
    'Салат №1 🥗',
    'Салат №2 🥗',
    'Чизкейк 🍓',
    'Чизкейк 🥥',
    'Чизкейк 🍫',
    'Чизкейк 🍌',
    'Чизкейк 🌰',
    'Чизкейк классик',
    'Сырники со сметаной',
    'Сырники со сгущенкой',
]
