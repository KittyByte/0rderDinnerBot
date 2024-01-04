import asyncio
from threading import Thread
from loader import dp, logging
from aiogram import executor
from services.send_to_time import scheduler
from services.user_bot import client


async def start_up(_):
    logging.info('Бот был запущен!')
    print('[+] Бот успешно запущен')


def bot_thread():
    # Создаем цикл событий в потоке
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    scheduler.start()
    executor.start_polling(dp, skip_updates=True, on_startup=start_up)


if __name__ == '__main__':
    try:
        bot_thread = Thread(target=bot_thread)
        bot_thread.daemon = True
        bot_thread.start()

        print('[+] Юзербот успешно запущен')
        client.run()
    except Exception as error:
        print(error)
    finally:
        print('\n[+] Пока пока...')
