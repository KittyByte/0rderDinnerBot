from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup
from loader import dinner_sets


cancel = ReplyKeyboardMarkup(resize_keyboard=True).add('Отменить действие 🚫')
del_kb = ReplyKeyboardRemove()

inline_user_manager = InlineKeyboardMarkup(row_width=2)
inline_user_manager.add(*[
    InlineKeyboardButton("Добавить", callback_data="add"),
    InlineKeyboardButton("Удалить", callback_data="remove"),
    InlineKeyboardButton("Отправить фото обеда 🥗", callback_data="send_photo"),
]).add(InlineKeyboardButton("Очистить обеды", callback_data="full_reset_meals"))

send_photo_yet = InlineKeyboardMarkup().add(InlineKeyboardButton("Отправить новое фото", callback_data="send_photo"))

add_user_admin = InlineKeyboardMarkup(row_width=2)
add_user_admin.add(*[
    InlineKeyboardButton("Админа", callback_data="add_admin"),
    InlineKeyboardButton("Пользователя", callback_data="add_user"),
    InlineKeyboardButton('Назад', callback_data='back_inline')
])


remove_user_admin = InlineKeyboardMarkup(row_width=2)
remove_user_admin.add(*[
    InlineKeyboardButton("Админа", callback_data="remove_admin"),
    InlineKeyboardButton("Пользователя", callback_data="remove_user"),
    InlineKeyboardButton('Назад', callback_data='back_inline')
])


def get_inline_dinner_buttons():
    inline_dinner_manager = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(value, callback_data=key) for key, value in dinner_sets().items()
    ]
    buttons.append(InlineKeyboardButton('Очистить мои заказы', callback_data='clear_my_meal'))
    inline_dinner_manager.add(*buttons)

    return inline_dinner_manager

