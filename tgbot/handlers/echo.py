from aiogram import types, Dispatcher


async def bot_echo(message: types.Message):
    text = [
        "неверная команда пожалуйста введите /help"
    ]

    await message.answer('\n'.join(text))


def register_echo(dp: Dispatcher):
    dp.register_message_handler(bot_echo)
