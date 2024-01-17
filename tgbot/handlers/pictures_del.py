import os.path
import os
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from tgbot.middlewares.DBhelp import BotDB
from tgbot.misc.states import all
from aiogram import Router, F
#ошибки 8000


router = Router()

length = 20     #длинна кодового слова для теста

@router.callback_query(F.data == "pictures_del", all.interface_all_stateQ1)    
async def pictures_del(call: types.CallbackQuery, state: FSMContext):
    try:
        Title_Test_code = BotDB.get_pictures_pictures_code(call.from_user.id)
        keyboard =  InlineKeyboardBuilder()
        all1 = "Коды картинок доступных для удаления\n"
        for a in Title_Test_code:
            button_h = types.InlineKeyboardButton(text = a[0], callback_data = a[0])
            keyboard.row(button_h)
        button_h = types.InlineKeyboardButton(text = "Отмена", callback_data = "start")
        keyboard.row(button_h)
        await call.message.answer(all1, reply_markup = keyboard.as_markup())
        await state.set_state(state=all.test_pictures_delQ1)
    except:
        await call.message.answer("Произошла ошибка 8001")
        await state.clear()

@router.callback_query(all.test_pictures_delQ1)    
async def pictures_del2(call: types.CallbackQuery, state: FSMContext):
    try:
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
            await state.clear()
            await pictures_del(call,state)
        else:
            pass
    except:
        await call.message.answer("Произошла ошибка 8002")
        await state.clear()