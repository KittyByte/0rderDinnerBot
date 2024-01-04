<div style="text-align:center;"><h1> 0rderDinnerBot</h1></div>
<p align="center">
  <img src="imgs\img.png" alt="img.png" width="350">
</p>

> **Это бот, для автоматизации заказа обедов в компании, основной функционал реализовывался для работы с группой @vokrugsveta_26.   
> Он предоставляет удобный способ для участников компании заказывать обеды и получать информацию о выбранных блюдах.**

> **Авторы: [KittyByte](https://github.com/KittyByte) и [yurikpetro](https://github.com/yurikpetro)**

## Возможности

- Автоматически парсит фото обедов с группы и отправляет в чат.
- Автоматически добавляет участников в БД по входу/выходу из чата.
- Собирает информацию о выбранных обедах по нажатию кнопок.
- Предоставляет информацию о количестве каждого выбранного блюда.
- Выводит список участников, кто не сделал заказ по команде /check.

## Стек технологий

- Python
- Aiogram2 (https://docs.aiogram.dev/)
- Pyrogram (https://docs.pyrogram.org/)
- APScheduler (https://apscheduler.readthedocs.io/)
- Threading

## Инструкция по развертыванию бота

1. Зарегистрируйте бота в Telegram с помощью @BotFather (https://t.me/BotFather) и получите API-токен бота.
2. Перейдите на Telegram Core API (https://core.telegram.org/api/obtaining_api_id) и зарегистрируйте свое приложение для получения API ID и API Hash.
3. Установите необходимые зависимости:
   ```sh
   pip install -r requirements.txt
   ```
4. Настройте config, замените параметры соответствующими вам значениями.
   ```
   # конфигурация бота
   BOT_TOKEN = 'токен вашего бота' #токен можно получить в шаге №1
   CHAT_RECIPIENT_ID = 'id группы, куда будут пересылаться спаренные фото с инлайн-кнопками' 
   
   # Настройка времени и дней для автоматической отправки
   TIME_TO_SEND_ORDER_HOUR = 9
   TIME_TO_SEND_ORDER_MINUTES = 0
   DAYS_OF_WEEK_TO_SEND = 'mon-fri'
   
   # Параметры для работы с userbot'ом. Эти данные можно получить в шаге №2
   USERBOT_API_ID = 12345
   USERBOT_API_HASH = 'abc12345'
   
   # id чата от куда парсится фото
   CHAT_ID_FOR_PARSING = -1001964895000
   ```

5. Перейдите в user_bot.py и измените его под ваши нужды, в нем находится логика парсинга изображений
6. В loader.py измените dinners_sets, переменные в нем будут отображаться на inline кнопках, а также они будут записываться в БД, они должны быть уникальными
7. Запустите бота.
8. Теперь ваш бот готов для автоматизации заказов обедов в компании!

---
### Команды доступные у бота:
  - /help - информацию по работе
  - /photo_status - отправляет в чат фото, сохранённые на сервере
  - /check - показывает кто не сделал заказы
---

## Пример работы бота: 
<p align="center">
  <img src="imgs\example3.jpg" alt="example2.jpg" width="350">
  <img src="imgs\example1.jpg" alt="example1.jpg" width="350">
  <img src="imgs\example2.jpg" alt="example2.jpg" width="350">
</p>

<div style="text-align:center;"><h1> Удачи с Вашим 0rderDinnerBot!</h1></div>
