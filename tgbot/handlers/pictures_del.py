import os.path
import os
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup
from tgbot.middlewares.DBhelp import BotDB
from tgbot.misc.states import all



length = 20     #длинна кодового слова для теста

async def pictures_del(call: types.CallbackQuery):
    Title_Test_code = BotDB.get_pictures_pictures_code(call.from_user.id)
    button =  InlineKeyboardMarkup()
    all1 = "Коды картинок доступных для удаления\n"
    for a in Title_Test_code:
        button_h = types.InlineKeyboardButton(a[0], callback_data = a[0])
        button.add(button_h)
    button_h = types.InlineKeyboardButton(("Отмена"), callback_data = "start")
    button.add(button_h)
    await call.message.answer(all1, reply_markup = button)
    await all.test_pictures_delQ1.set()


async def pictures_del2(call: types.CallbackQuery, state: FSMContext):
    flag = 0
    Title_Test_code = BotDB.get_pictures_pictures_code(call.from_user.id)
    for a in Title_Test_code:
        if a[0] == str(call.data):
            flag = 1
    if flag == 1:
        photo_adres = os.path.join(".","pictures",call.data+".png")
        os.remove(photo_adres)
        BotDB.pictures_del(call.data)
        await call.message.answer("Картинка с кодом " + call.data + " удалена")
        await state.finish()
        await pictures_del(call)
    else:
        pass


def register_pictures_del(dp: Dispatcher):
    dp.register_callback_query_handler(pictures_del, lambda c: c.data == "pictures_del",state=all.interface_all_stateQ1)
    dp.register_callback_query_handler(pictures_del2, state=all.test_pictures_delQ1)