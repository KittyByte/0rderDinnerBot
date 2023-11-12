from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers import send_photo_and_state
from config import (
    TIME_TO_SEND_ORDER_HOUR,
    TIME_TO_SEND_ORDER_MINUTES,
    DAYS_OF_WEEK_TO_SEND,
)

# Модуль вызова метода по расписанию
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

scheduler.add_job(
    send_photo_and_state,
    trigger='cron',
    hour=TIME_TO_SEND_ORDER_HOUR,
    minute=TIME_TO_SEND_ORDER_MINUTES,
    start_date=datetime.now(),
    day_of_week=DAYS_OF_WEEK_TO_SEND
)
