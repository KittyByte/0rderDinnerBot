from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from services.ocr import ocr

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)

log_name = 'logs.log'
logging.basicConfig(
    filename=log_name,
    filemode='w',
    format='[%(asctime)s.%(msecs)-3d] %(filename)s:%(lineno)d #%(levelname)s - %(message)s',  # -25s это отступы
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


class __DinnerSetsLoader:
    def __init__(self):
        self.__base_set = [
            'Чизкейк 🍓',
            'Чизкейк 🥥',
            'Чизкейк 🍫',
            'Чизкейк 🍌',
            'Чизкейк 🌰',
            'Чизкейк классик',
            'Сырники со сметаной',
            'Сырники со сгущенкой',
            'Хлеб белый ◻️',
            'Хлеб черный ⬛️'
        ]
        self.dinners_sets: dict = self.__get_dinner_sets()  # тут хранятся значения при первой инициализации класса, для последующего обновления значений необходимо вызывать метод

    def __call__(self):
        return self.dinners_sets

    def __get_base_set(self):
        dinners_sets = [
            'Суп №1 🍜',
            'Суп №2 🍜',
            'Второе №1 🍱',
            'Второе №2 🍱',
            'Салат №1 🥗',
            'Салат №2 🥗',
        ] + self.__base_set
        return dinners_sets

    def __get_dinner_sets(self) -> dict:
        __dinners_sets_list = ocr.img_to_text()

        if __dinners_sets_list:
            __dinners_sets_list.extend(self.__base_set)
            dinners_sets = {num: meal for num, meal in enumerate(__dinners_sets_list)}
        else:
            logging.warning(f'Ошибка - {__dinners_sets_list}')
            dinners_sets = self.__get_base_set()

        return dinners_sets

    def update_dinner_sets(self):
        self.dinners_sets = self.__get_dinner_sets()
        logging.info(f'Установленны кнопки - {self.dinners_sets}')


dinner_sets = __DinnerSetsLoader()
