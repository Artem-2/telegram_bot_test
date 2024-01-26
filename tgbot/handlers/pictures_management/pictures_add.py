import os.path
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, F
from tgbot.middlewares.DBhelp import BotDB
from tgbot.misc.states import all
from tgbot.misc.deleting_last_messages import deleting_last_messages
from tgbot.handlers.interface_all import interface_all_begin
import random
import string
#ошибки 7000

router = Router()


length = 20     #длинна кодового слова для теста

@router.callback_query(F.data == "pictures", all.interface_all_stateQ1)
async def pictures(call: types.CallbackQuery, state: FSMContext):
    try:
        keyboard =  InlineKeyboardBuilder()
        button_h = types.InlineKeyboardButton(text="Отмена", callback_data="start")
        keyboard.row(button_h)
        await deleting_last_messages(state)
        last_message = await call.message.answer("Отправьте фотографию которую необходимо добавить в тест",reply_markup = keyboard.as_markup())
        await state.update_data(last_message=last_message)
        await state.set_state(state=all.test_picturesQ1)
    except:
        await call.message.answer("Произошла ошибка 7001")
        await state.clear()


@router.message(F.photo, all.test_picturesQ1)
async def pictures3(message: types.Message, state: FSMContext):
    try:
        result = 1
        while result != None:
            letters = string.ascii_uppercase
            rand_string = ''.join(random.choice(letters) for i in range(length))
            result = BotDB.get_pictures_id(rand_string)
        
        await deleting_last_messages(state)
        await message.answer("Код картинки : " + rand_string)

        photo_adres = os.path.join(".","pictures",rand_string+".png")

        await message.bot.download(file=message.photo[-1].file_id, destination=photo_adres)

        BotDB.pictures_add(rand_string, message.from_user.id)
        await message.answer("Фото добавлено в базу")
        await state.clear()
        await interface_all_begin(message, state)
    except:
        await message.answer("Произошла ошибка 7002")
        await state.clear()
