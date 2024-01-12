import asyncio
import logging 

from tgbot.handlers import interface_all

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy
from aiogram.client.session.aiohttp import AiohttpSession

from tgbot.config import config



logger = logging.getLogger(__name__)




async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")

    
    storage = MemoryStorage()
    session = AiohttpSession(proxy=config.tg_bot.proxy)
    bot = Bot(token=config.tg_bot.token, session=session, parse_mode='HTML')
    dp = Dispatcher(storage=storage, fsm_strategy=FSMStrategy.GLOBAL_USER)
    dp.include_routers(interface_all.router)


    try:
        for c in config.tg_bot.admin_ids:
            await bot.send_message(c,'Бот запущен')
    except:
        print("Неверный id админа \n")
    # Start
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        try:
            for c in config.tg_bot.admin_ids:
                await bot.send_message(c,'Бот отключен')
        except:
            pass
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
