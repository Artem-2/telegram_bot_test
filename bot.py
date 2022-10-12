import asyncio
import logging 

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import bot 
from tgbot.config import dp
from tgbot.config import config2
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.rename import register_user_rename
from tgbot.handlers.test_create import register_test_create
from tgbot.handlers.test_del import register_test_del
from tgbot.handlers.registration import register_Registration
from tgbot.handlers.pictures import register_pictures
from tgbot.handlers.pictures_del import register_pictures_del
from tgbot.handlers.get_test_result_admin import register_get_test_result_admin
from tgbot.handlers.get_test_result import register_get_test_result
from tgbot.handlers.get_test_result_one_day import register_get_test_result_one_day
from tgbot.handlers.activete_deactivete import register_activete
from tgbot.handlers.passing_the_test import register_passing_the_test
from tgbot.handlers.interface_all import register_interface_all
from tgbot.handlers.registration_teachers import register_registration_teachers
#from tgbot.middlewares.DBhelp import DbMiddleware 




logger = logging.getLogger(__name__)


def register_all_middlewares(dp):
    pass
    #dp.setup_middleware(DbMiddleware())


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_registration_teachers(dp)
    register_user_rename(dp)
    register_pictures(dp)
    register_test_create(dp)
    register_Registration(dp)
    register_passing_the_test(dp)
    register_interface_all(dp)
    register_get_test_result_admin(dp)
    register_get_test_result(dp)
    register_get_test_result_one_day(dp)
    register_test_del(dp)
    register_activete(dp)
    register_pictures_del(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")

    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    try:
        for c in config2.tg_bot.admin_ids:
            await bot.send_message(c,'Бот запущен')
    except:
        print("Неверный id админа \n")
    # Start
    try:
        await dp.start_polling()
    finally:
        try:
            for c in config2.tg_bot.admin_ids:
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
