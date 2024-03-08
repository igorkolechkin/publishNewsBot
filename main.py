import asyncio
import logging
import pytz
import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher
from message.warship.request_to_api import get_warship_info

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()


async def hello_job() -> None:
    text_hello = 'Доброго ранку, друзі! 🇺🇦🫡'

    try:
        await bot.send_message(config.CHAT_ID, text_hello, parse_mode='HTML')
    except Exception as e:
        print(f"Произошла ошибка: {e}")


async def warship_job(time_of_day: str) -> None:
    warship_info = get_warship_info(time_of_day)

    try:
        await bot.send_message(config.CHAT_ID, warship_info, parse_mode='HTML')
    except Exception as e:
        print(f"Произошла ошибка: {e}")


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    scheduler = AsyncIOScheduler(timezone=pytz.timezone('Europe/Kiev'))
    scheduler.add_job(hello_job, 'cron', hour=9, minute=30)
    scheduler.add_job(warship_job, 'cron', hour=10, minute=0, args=['ранок'])
    scheduler.start()

    while True:
        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
