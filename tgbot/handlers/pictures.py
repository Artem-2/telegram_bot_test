import os.path
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup
from tgbot.middlewares.DBhelp import BotDB
from tgbot.misc.states import all
from tgbot.handlers.interface_all import interface_all_begin
import random
import string



length = 20     #длинна кодового слова для теста

async def pictures(call: types.CallbackQuery):
    button =  InlineKeyboardMarkup()
    button_h = types.InlineKeyboardButton(text="Отмена", callback_data="start")
    button.add(button_h)
    await call.message.answer("Отправьте фотографию которую необходимо добавить в тест",reply_markup = button)
    await all.test_picturesQ1.set()


async def pictures3(message: types.Message, state: FSMContext):
    result = 1
    while result != None:
        letters = string.ascii_uppercase
        rand_string = ''.join(random.choice(letters) for i in range(length))
        result = BotDB.get_pictures_id(rand_string)
        
    await message.answer("Код картинки : " + rand_string)
    photo = message.photo.pop()
    photo_adres = os.path.join(".","pictures",rand_string+".png")
    await photo.download(photo_adres)
    BotDB.pictures_add(rand_string, message.from_user.id)
    await message.answer("Фото добавлено в базу")
    await state.finish()
    await interface_all_begin(message, state)


def register_pictures(dp: Dispatcher):
    dp.register_callback_query_handler(pictures, lambda c: c.data == "pictures", state=None)
    dp.register_message_handler(pictures3,content_types = ['photo'], state=all.test_picturesQ1)