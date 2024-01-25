from loader import logging
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from config import USERBOT_API_HASH, USERBOT_API_ID, CHAT_ID_FOR_PARSING


logging.getLogger("pyrogram").setLevel(logging.WARNING)
client = Client(name='my_bot', api_id=USERBOT_API_ID, api_hash=USERBOT_API_HASH)
last_photos_id = []


async def message_photo(client: Client, message):  # передаём в функцию ID или Username чата
    global last_photos_id
    async for msg in client.get_chat_history(chat_id=CHAT_ID_FOR_PARSING, limit=3, offset_id=-1):  # ищем в истории с конца
        if msg.photo:
            logging.info(f'В группу было отправлено фото msg_id={msg.id}')
            msg_caption = str(msg.caption).split("\n")
            if msg.id not in last_photos_id:
                last_photos_id.append(msg.id)
                if "Доставка обедов" in msg.caption:  # если есть фото и оно подходит по описанию
                    await client.download_media(msg.photo, file_name=f'order.jpg')
                    logging.info(f'Фото меню msg_id={msg.id} | Описание: {msg_caption} сохранено')
                elif "Обед дня №1" in msg.caption:
                    await client.download_media(msg.photo, file_name=f'dinner_1.jpg')
                    logging.info(f'Фото обеда №1 msg_id={msg.id} | Описание: {msg_caption} сохранено')
                elif "Обед дня №2" in msg.caption:
                    await client.download_media(msg.photo, file_name=f'dinner_2.jpg')
                    logging.info(f'Фото обеда №2 msg_id={msg.id} | Описание: {msg_caption} сохранено')
            else:
                logging.warning(f'Фото с таким msg_id={msg.id} уже сохранено')

client.add_handler(MessageHandler(message_photo, filters=filters.photo & filters.chat(chats=CHAT_ID_FOR_PARSING)))
