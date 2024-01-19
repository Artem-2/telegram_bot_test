import asyncio
import logging 
import sys

from tgbot.handlers import interface_all
from tgbot.handlers import activete_deactivete
from tgbot.handlers import get_test_result_admin
from tgbot.handlers import get_test_result_one_day
from tgbot.handlers import get_test_result
from tgbot.handlers import passing_the_test_v2
from tgbot.handlers import test_create
from tgbot.handlers import pictures_del
from tgbot.handlers import registration
from tgbot.handlers import registration_teachers
from tgbot.handlers import pictures
from tgbot.handlers import rename
from tgbot.handlers import test_del


from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy
from aiogram.client.session.aiohttp import AiohttpSession

from tgbot.misc.config import config



logger = logging.getLogger(__name__)




async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")

    storage = MemoryStorage()
    
    if config.tg_bot.proxy == "None":
        bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    else:
        session = AiohttpSession(proxy=config.tg_bot.proxy)
        bot = Bot(token=config.tg_bot.token, session=session, parse_mode='HTML')
    dp = Dispatcher(storage=storage, fsm_strategy=FSMStrategy.GLOBAL_USER)
    
    dp.include_routers(get_test_result_admin.router)
    dp.include_routers(passing_the_test_v2.router)
    dp.include_routers(test_create.router)
    dp.include_routers(registration.router)
    dp.include_routers(registration_teachers.router)
    dp.include_routers(interface_all.router)
    dp.include_routers(get_test_result.router)
    dp.include_routers(pictures_del.router)
    dp.include_routers(test_del.router)
    dp.include_routers(activete_deactivete.router)
    dp.include_routers(get_test_result_one_day.router)
    dp.include_routers(pictures.router)
    dp.include_routers(rename.router)


    try:
        for c in config.tg_bot.admin_ids:
            await bot.send_message(c,'Бот запущен')
    except:
        sys.exit("Неверный id админа \n")
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
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
