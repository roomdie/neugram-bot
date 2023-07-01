import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from . import middlewares, handlers, filters
from . import config
from .services import commands_setter, admin_notificator, logger


async def main():
    """
     Важно! В данный момент контекст будет в оперативной памяти и при перезапуске бота,
     данные будут сброшены. Чтобы данные контекста чата сохранялись, вам нужен Redis.

    storage = RedisStorage2(host=config.REDIS_HOST, password=config.REDIS_PASSWORD, port=6379, db=0)
    """

    bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    middlewares.setup(dp)
    filters.setup(dp)
    handlers.setup(dp)

    bot["dp"] = dp

    await commands_setter.set_bot_commands(dp)
    await admin_notificator.notify(dp)
    _bot = await bot.get_me()

    logging.info(f"Bot: @{_bot.username}")

    try:
        # await dp.skip_updates()   в production режиме лучше не включать
        await dp.start_polling(allowed_updates=types.AllowedUpdates.all())
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
