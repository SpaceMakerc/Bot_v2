from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import asyncio
import logging

from src.core import settings
from routers import router


async def main():
    dp = Dispatcher()
    dp.include_router(router)

    logging.basicConfig(level=logging.INFO)
    bot = Bot(
        token=settings.token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
