from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, Message, CallbackQuery, ParseMode, InputFile, MediaGroup
from keyboards import *
from loader import dp, bot, States, logging
from config import CHAT_RECIPIENT_ID
from services.connection_db import db

msg_to_update_group = ''  # id сообщения, показывающее статус заказов в группе

# -----------------------------------------------------------------------
def admin_in_bd(tg_id) -> bool:
    if tg_id in db.get_admins():
        return True
    return False

def user_in_bd(tg_id) -> bool:
    if str(tg_id) in db.get_users().keys():
        return True
    return False

async def reset_meal():
    db.reset_meals()
    logging.info('Запущен сброс обедов')
# -----------------------------------------------------------------------


@dp.message_handler(content_types=[ContentType.NEW_CHAT_MEMBERS, ContentType.LEFT_CHAT_MEMBER])
async def on_chat_membership_change(message: Message):
    """ Добавляет приходящих и удаляет уходящих участников """
    if message.content_type == 'new_chat_members' and not message.from_user.is_bot:
        for user in message.new_chat_members:
            user_id = user.id
            username = user.username
            first_name = user.first_name
            await message.reply(f"Добавлен новый участник: ID: {user_id}, Имя: {first_name}, Username: @{username}")
            db.add_user(user_id, username, first_name)

    elif message.content_type == 'left_chat_member':
        user = message.left_chat_member
        user_id = user.id
        username = user.username
        first_name = user.first_name
        await message.reply(f"Участник покинул группу: ID: {user_id}, Имя: {first_name}, Username: @{username}")
        db.remove_user(user_id)


# --------------------------- Работа с командами ----------------------------------------------
async def show_users_admins(chat_id, user_id):
    result = 'Список пользователей:\n'
    for tg_id, data in db.get_users().items():
        username = '@None' if data[0] == 'null' else f'@{data[0]}'
        result += f'ID: <code>{tg_id}</code>, Имя: {data[1]}, {username}\n'

    result += '\nСписок админов:\n'
    for tg_id in db.get_admins():
        result += f'ID: <code>{tg_id}</code>\n'

    result += '\n /help - Помощь по боту'

    await bot.send_message(chat_id, result, parse_mode=ParseMode.HTML, reply_markup=inline_user_manager if admin_in_bd(user_id) else None)


@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    user_id = message.from_user.id
    # бот работает только с теми кто в базе данных
    if admin_in_bd(user_id) or user_in_bd(user_id):
        await message.reply(text="Привет! Я OrderDinnerBot! Я помогу автоматизировать заказ обедов в твоей компании. "
                                 "Чтобы узнать больше обо мне отправь команду /help", reply_markup=del_kb)
        if "-" not in str(message.chat.id):
            await show_users_admins(message.chat.id, user_id)
    else:
        await message.reply(text="Привет! Я OrderDinnerBot! Я помогу автоматизировать заказ обедов в твоей компании.\n"
                                 "Для взаимодействия со мной нужно состоять в чате заказа обедов.", reply_markup=del_kb)


@dp.message_handler(commands=['help'])
async def start_command(message: Message):
    text = '''/start - вызывает главное меню бота
Статья как получить ID пользователя - https://nastroyvse.ru/programs/review/telegram-id-kak-uznat-zachem-nuzhno.html
/check - используется для вывода имен пользователей, не сделавших заказ
"Кнопкой "отправить фото обеда" вы отправляете фото обеда в группу, а также получаете сообщение о статусе заказов 
Кнопка "Очистить обеды" очищает обеды всех пользователей
'''
    await message.reply(text)


@dp.message_handler(commands=['check'])
async def start_command(message: Message):
    """ Вывод имен пользователей не сделавших заказ """
    user_id = message.from_user.id
    names_without_order = [user[1] for user in db.get_users().values() if user[2] == []]  # Получение списка имен без заказа
    enum_names = [f'{index}. {user}\n' for index, user in enumerate(names_without_order, 1)]
    if admin_in_bd(user_id) or user_in_bd(user_id):
        await message.reply(f'Пользователи, не сделавшие заказ:\n{"".join(enum_names)}')
    else:
        await message.reply('Для использования этой команды нужно нужно состоять в чате заказа обедов.')
# --------------------------- Работа с командами конец ----------------------------------------------


# --------------------------- Работа с состояниями ----------------------------------------------
@dp.message_handler(text=['Отменить действие 🚫'], state='*')
async def cancel_current_state(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await message.reply('Действие отменено', reply_markup=del_kb)
    await state.finish()


@dp.message_handler(state=States.all_states)
async def handle_generic_operation(message: Message, state: FSMContext):
    """ Вызывает метода исходя из установленного состояния """
    current_state = await state.get_state()

    if current_state == 'States:user_add':
        await handle_user_add(message, state)
    elif current_state == 'States:user_remove':
        await handle_user_remove(message, state)
    elif current_state == 'States:admin_add':
        await handle_admin_add(message, state)
    elif current_state == 'States:admin_remove':
        await handle_admin_remove(message, state)


async def handle_user_add(message: Message, state: FSMContext):
    msg = message.text.split(' ')
    tg_id, tg_username, tg_name = msg[0], msg[1].replace('@', ''), ' '.join(msg[2:])
    if db.add_user(tg_id, tg_username, tg_name) and message.from_user.is_bot is False:
        tg_username = f'@None' if tg_username == '-' else f'@{tg_username}'
        await message.reply(f'Пользователь {tg_id} {tg_username} {tg_name} добавлен', reply_markup=del_kb)
    else:
        await message.reply('Ошибка!', reply_markup=del_kb)

    await state.finish()


async def handle_user_remove(message: Message, state: FSMContext):
    if db.remove_user(message.text):
        await message.reply(f'Пользователь с ID {message.text} удален', reply_markup=del_kb)
    else:
        await message.reply('Ошибка!', reply_markup=del_kb)

    await state.finish()


async def handle_admin_add(message: Message, state: FSMContext):
    if db.add_admin(message.text):
        await message.reply(f'Пользователь ID {message.text} стал админом', reply_markup=del_kb)
    else:
        await message.reply('Неверно введен ID', reply_markup=del_kb)

    await state.finish()


async def handle_admin_remove(message: Message, state: FSMContext):
    if db.remove_admin(message.text):
        await message.reply(f'ID {message.text} убран из админов', reply_markup=del_kb)
    else:
        await message.reply('Неверно введен ID или такого админа нет', reply_markup=del_kb)

    await state.finish()


@dp.message_handler(state=States.photo_to_send, content_types=ContentType.PHOTO)  # тип фото обязательно, ибо по умолчанию она его не принимает
async def handle_photo_resend(message: Message, state: FSMContext):
    global msg_to_update_group
    photo_id = message.photo[-1].file_id  # Получаем последнюю (наибольшего размера) фотографию
    db.reset_meals()

    await bot.send_photo(chat_id=CHAT_RECIPIENT_ID, photo=photo_id, reply_markup=inline_dinner_manager)
    msg = await bot.send_message(chat_id=CHAT_RECIPIENT_ID, text='Кто сделал заказы:')
    msg_to_update_group = msg.message_id
    await message.reply('Фото успешно отправлено', reply_markup=del_kb)
    await bot.send_message(message.chat.id, 'Отправить ещё одно фото?', reply_markup=send_photo_yet)

    await update_message()
    await state.finish()
# --------------------------- Работа с состояниями конец ----------------------------------------------


async def send_photo_and_state():
    """ Отвечает за отправку фото, состояния заказа и кнопок по установленному времени """
    global msg_to_update_group

    await reset_meal()

    media = MediaGroup()
    media.attach_photo(InputFile('downloads/dinner_1.jpg'), caption='Обед дня №1')
    media.attach_photo(InputFile('downloads/dinner_2.jpg'), caption='Обед дня №2')
    await bot.send_media_group(CHAT_RECIPIENT_ID, media=media)
    logging.info('Фото обедов №1 и №2 отправлены')

    logging.info('Запуск отправки фото в группу по расписанию')
    with open('downloads/order.jpg', 'rb') as photo:
        await bot.send_photo(chat_id=CHAT_RECIPIENT_ID, photo=photo,
                             caption="🍲🍝🥗Доставка обедов🥗🍝🍲",
                             reply_markup=inline_dinner_manager)
        msg = await bot.send_message(
            chat_id=CHAT_RECIPIENT_ID,
            text='Кто сделал заказы:'
        )
        msg_to_update_group = msg.message_id

    await update_message()


async def update_message():
    new_meal = 'Кто сделал заказы:\n' + db.get_usr_meal()  # статус заказов отображаемый в группе

    order_status = 'Текущий статус заказов:\n'  # статус заказов отправляемый админу
    for name_meal, count in db.get_order_status().items():
        if count:
            order_status += f'{name_meal} - {count}\n'
    order_status += f'Количество приборов - {db.get_tools()}'
    try:
        await bot.edit_message_text(chat_id=CHAT_RECIPIENT_ID, message_id=msg_to_update_group,
                                    text=f'{new_meal}\n{order_status}')
    except Exception:
        logging.warning(f'Не удалось отредактировать сообщение msg_to_update_group -> {msg_to_update_group}')


# ----------------------- обработчики inline кнопок ----------------------------
@dp.callback_query_handler()
async def query_add_user(call: CallbackQuery):
    call_id = call.from_user.id
    if not user_in_bd(call_id):
        await call.answer('Вас нет в списке участников для заказа обедов, обратитесь к администратору за запросом', show_alert=True)
        return

    messages_and_states = {
        'add_user': ('Введите ID username Имя кого вы хотите добавить\nПример: 454757546 @vasiliy Василий\nУкажите " - " если нет @username\nПример: 454757546 - Василий', States.user_add),
        'add_admin': ('Введите ID кого вы хотите добавить в админы\nПример: 454757546', States.admin_add),
        'remove_user': ('Введите ID пользователя кого вы хотите удалить\nПример: 454757546', States.user_remove),
        'remove_admin': ('Введите ID кого вы хотите удалить из админов\nПример: 454757546', States.admin_remove),
        'send_photo': ('Пришлите фото', States.photo_to_send),
    }

    if call.data == 'clear_my_meal':  # сбрасывает обед того кто его нажал
        db.del_my_meal(call.from_user.id)
        await update_message()
        await bot.answer_callback_query(call.id)

    if call.data in dinners_sets and msg_to_update_group:  # message_to_update_group - защита от нажатия по старым сообщениям с кнопками
        db.set_meal(call.from_user.id, call.data)
        await update_message()
        await bot.answer_callback_query(call.id)

    # ---------------- Обработчики админских кнопок ------------------------
    if not admin_in_bd(call_id): await call.answer('Вы не админ'); return

    if call.data in messages_and_states:
        message, state = messages_and_states[call.data]
        await bot.send_message(call_id, text=message, reply_markup=cancel)
        await state.set()

    if call.data == 'full_reset_meals':  # срабатывает при нажатии кнопки сброса всех обедов в админке
        db.reset_meals()
        await bot.send_message(call_id, text='Все обеды сброшены')
        await update_message()
        await bot.answer_callback_query(call.id)

    if call.data == 'add':
        await call.message.edit_reply_markup(reply_markup=add_user_admin)
    elif call.data == 'remove':
        await call.message.edit_reply_markup(reply_markup=remove_user_admin)
    elif call.data == 'back_inline':
        await call.message.edit_reply_markup(reply_markup=inline_user_manager)
