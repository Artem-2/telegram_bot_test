from aiogram import Dispatcher
from aiogram.types import Message


async def user_help(message: Message):
    await message.reply("- Перед прохождением теста необходимо пройти регистрацию, введя /registration\n- Изменить имя пользователя /rename\n- Для прохождения теста введите /test\n\n- Для создания теста введите /test_create\n- Добавить новую картинку в бацу /pictures\n- Чтобы получить инструкцию для создания теста, введите /test_create_help\n- Для получения результатов теста введите /get_test_result (для создателей!!!)\n- Удалить тест /test_del (для создателей!!!)\n- Активировать тест /activete\n- Отключить тест /deactivete")


def register_help(dp: Dispatcher):
    dp.register_message_handler(user_help, commands=["help"], state="*")
