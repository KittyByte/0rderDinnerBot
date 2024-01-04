from loader import logging
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from config import USERBOT_API_HASH, USERBOT_API_ID, CHAT_ID_FOR_PARSING


client = Client(name='my_bot', api_id=USERBOT_API_ID, api_hash=USERBOT_API_HASH)
last_photo_id = None


async def message_photo(client: Client, message):  # передаём в функцию ID или Username чата
    global last_photo_id
    async for msg in client.get_chat_history(chat_id=CHAT_ID_FOR_PARSING, limit=3, offset_id=-1):  # ищем в истории с конца
        if msg.photo:
            logging.info(f'В группу было отправлено фото {msg.photo.file_id}')
            if "Доставка обедов" in msg.caption:  # если есть фото и оно подходит по описанию
                if msg.photo.file_id != last_photo_id:  # Если id нового фото не такой, как у предыдущего, то загружаем его
                    await client.download_media(msg.photo, file_name=f'order.jpg')  # Загружаем фото
                    last_photo_id = msg.photo.file_id
                    logging.info(f'Новое фото {msg.photo.file_id} было сохранено')
            elif "Обед дня №1" in msg.caption:
                await client.download_media(msg.photo, file_name=f'dinner_1.jpg')
                logging.info(f'Фото обеда №1 {msg.photo.file_id} (dinner_1.jpg) было сохранено')
            elif "Обед дня №2" in msg.caption:
                await client.download_media(msg.photo, file_name=f'dinner_2.jpg')
                logging.info(f'Фото обеда №2 {msg.photo.file_id} (dinner_2.jpg) было сохранено')

client.add_handler(MessageHandler(message_photo, filters=filters.photo & filters.chat(chats=int(CHAT_ID_FOR_PARSING))))
