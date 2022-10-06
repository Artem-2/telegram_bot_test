from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup
from tgbot.middlewares.DBhelp import BotDB
from tgbot.misc.states import all
from tgbot.handlers.interface_all import interface_all_begin2
#ошибки 9400





async def test_del1(call: types.CallbackQuery, state: FSMContext):
    try:
        Title_Test_code = BotDB.get_test_title_test_code_no_active_mode(call.from_user.id)
        button =  InlineKeyboardMarkup()
        all1 = "Тесты которыe вы можете удалить:\n"
        for a in Title_Test_code:
            all1 = all1 + "\n" + "Код теста: " + a[1] + "\n" + "Название теста: " + a[0]
            button_h = types.InlineKeyboardButton((a[1]), callback_data = a[1])
            button.add(button_h)
        button_h = types.InlineKeyboardButton(("Отмена"), callback_data = "start")
        button.add(button_h)
        await call.message.answer(all1, reply_markup = button)
        await all.test_del_stateQ1.set()
    except:
        await call.message.answer("Произошла ошибка 9401")
        await state.finish()



async def test_del2(call: types.CallbackQuery, state: FSMContext):
    try:
        flag = 0
        Title_Test_code = BotDB.get_test_title_test_code_no_active_mode(call.from_user.id)
        for a in Title_Test_code:
            if a[1] == str(call.data):
                flag = 1
        if flag == 1:
            a = BotDB.get_test_user_create_id(int(call.from_user.id), str(call.data))
            async with state.proxy() as data:
                data["test_id_del"] = a[0][0]
            button =  InlineKeyboardMarkup()
            button_h = types.InlineKeyboardButton(("Продолжить"), callback_data = "test_del_activate")
            button.add(button_h)
            button_h = types.InlineKeyboardButton(("Отмена"), callback_data = "start")
            button.add(button_h)
            await call.message.answer("Код теста который будет удален:" + str(call.data), reply_markup = button)
            await all.test_del_stateQ2.set()
        else:
            pass
    except:
        await call.message.answer("Произошла ошибка 9402")
        await state.finish()


async def test_del3(call: types.CallbackQuery, state: FSMContext):
    try:
        if call.data == "test_del_activate":
            async with state.proxy() as data:
                a = data["test_id_del"]
            BotDB.test_del(a)
            await call.message.answer("Тест удален")
            await state.finish()
            await interface_all_begin2(call, state)
        else:
            pass
    except:
        await call.message.answer("Произошла ошибка 9403")
        await state.finish()




def register_test_del(dp: Dispatcher):
    dp.register_callback_query_handler(test_del1,lambda c: c.data == "test_del", state=all.interface_all_stateQ1)
    dp.register_callback_query_handler(test_del2, state=all.test_del_stateQ1)
    dp.register_callback_query_handler(test_del3, lambda c: c.data == "test_del_activate", state=all.test_del_stateQ2)