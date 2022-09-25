
from aiogram import Dispatcher
from aiogram.types import Message


async def user_start(message: Message):
    await message.reply("Перед использованием бота введите /help")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
