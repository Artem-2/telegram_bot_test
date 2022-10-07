import asyncio
import xlwt
import os
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from tgbot.middlewares.DBhelp import BotDB
from tgbot.handlers.get_test_result import get_test_result2
from tgbot.misc.states import all, test_status, rename_state, reg_us
from aiogram.types import InlineKeyboardMarkup
from tgbot.handlers.interface_all import interface_all_begin2
#ошибки 3000





async def get_test_result_admin(call: types.CallbackQuery, state: FSMContext):
    try:
        Title_Test_code = BotDB.get_test_title_test_code_no_active_mode_admin()
        button =  InlineKeyboardMarkup()
        all1 = "Тесты, данные о которых вы можете получить\n"
        for a in Title_Test_code:
            user_name = BotDB.get_teachers_name(a[2])
            all1 = all1 + "\nКод теста: " + a[1] + "\nНазвание теста: " + a[0] + "\nСоздатель: " + user_name[0] + "\n"
            button_h = types.InlineKeyboardButton((a[1]), callback_data = a[1])
            button.add(button_h)
        button_h = types.InlineKeyboardButton(("Отмена"), callback_data = "start")
        button.add(button_h)
        await call.message.answer(all1, reply_markup = button)
        await all.get_test_adminQ1.set()
    except:
        await call.message.answer("Произошла ошибка 3001")
        await state.finish()


async def get_test_result_admin2(call: types.CallbackQuery, state: FSMContext):
    try:
        flag = 0
        Title_Test_code = BotDB.get_test_title_test_code_no_active_mode_admin()
        i = 0
        for a in Title_Test_code:
            if a[1] == str(call.data):
                flag = 1
        if flag == 1:
            await get_test_result2(call, state, admin = True)
        else:
            pass
    except:
        await call.message.answer("Произошла ошибка 3002")
        await state.finish()




def register_get_test_result_admin(dp: Dispatcher):
    dp.register_callback_query_handler(get_test_result_admin,lambda c: c.data == "get_test_result_admin", state=all.interface_all_stateQ1)
    dp.register_callback_query_handler(get_test_result_admin2, state=all.get_test_adminQ1)