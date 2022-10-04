from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

import datetime
from aiogram.types import InlineKeyboardMarkup
from tgbot.middlewares.DBhelp import BotDB
from tgbot.misc.states import all
from tgbot.handlers.interface_all import interface_all_begin2

    
    


async def get_test_result_one_day(call: types.CallbackQuery):
    Title_Test_code = BotDB.get_test_title_test_code_no_active_mode(call.from_user.id)
    button =  InlineKeyboardMarkup()
    all1 = "Тесты, данные о которых вы можете получить\n"
    for a in Title_Test_code:
        all1 = all1 + "\n" + "Код теста: " + a[1] + "\n" + "Название теста: " + a[0]
        button_h = types.InlineKeyboardButton((a[1]), callback_data = a[1])
        button.add(button_h)
    button_h = types.InlineKeyboardButton(("Отмена"), callback_data = "start")
    button.add(button_h)
    await call.message.answer(all1, reply_markup = button)
    await all.register_get_test_result_one_dayQ1.set()

async def get_test_result_one_day2(call: types.CallbackQuery, state: FSMContext):
    flag = 0
    Title_Test_code = BotDB.get_test_title_test_code_no_active_mode(call.from_user.id)
    for a in Title_Test_code:
        if a[1] == str(call.data):
            flag = 1
    if flag == 1:
        test_id = BotDB.get_test_user_create_id(int(call.from_user.id), str(call.data))
        res = BotDB.get_test_result_all(test_id[0][0])
        data_2 = datetime.datetime.now()
        for r in res:
            data = datetime.datetime.strptime(r[3], '%Y-%m-%d %H:%M:%S')
            data_3 = data_2 - data
            if data_3.days < 1:
                text = ""
                user_id = r[0]
                user_date = BotDB.get_user(user_id)
                text = text + "Группа: " + user_date[1] + "\n"
                text = text + "Фамилия Имя: " + user_date[0] + "\n"
                text = text + "Количество верных ответов/общее количество ответов: " + r[1] + "\n"
                text = text + "Оценка: " + str(r[2])
                await call.message.answer(text)
        await state.finish()
        await interface_all_begin2(call, state)
    else:
        pass

    
def register_get_test_result_one_day(dp: Dispatcher):
    dp.register_callback_query_handler(get_test_result_one_day, lambda c: c.data == "get_test_result_one_day", state=all.interface_all_stateQ1)
    dp.register_callback_query_handler(get_test_result_one_day2, state=all.register_get_test_result_one_dayQ1)