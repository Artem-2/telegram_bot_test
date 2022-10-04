from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from aiogram.types import InlineKeyboardMarkup
from tgbot.middlewares.DBhelp import BotDB
from tgbot.misc.states import all
from tgbot.handlers.interface_all import interface_all_begin2

    
    


async def activete(call: types.CallbackQuery):
    Title_Test_code = BotDB.get_test_title_code_test(call.from_user.id, False)
    button =  InlineKeyboardMarkup()
    all1 = "Тесты доступные для активации\n"
    for a in Title_Test_code:
        all1 = all1 + "\n" + "Код теста: " + a[1] + "\n" + "Название теста: " + a[0]
        button_h = types.InlineKeyboardButton((a[1]), callback_data = a[1])
        button.add(button_h)
    button_h = types.InlineKeyboardButton(("Отмена"), callback_data = "start")
    button.add(button_h)
    await call.message.answer(all1, reply_markup = button)
    await all.test_activateQ1.set()


async def activete2(call: types.CallbackQuery, state: FSMContext):
    flag = 0
    Title_Test_code = BotDB.get_test_title_code_test(call.from_user.id, False)
    for a in Title_Test_code:
        if a[1] == str(call.data):
            flag = 1
    if flag == 1:
        BotDB.test_update_active_mode(call.data, True)
        await call.message.answer("Тест с кодом " + str(call.data) + " активирован")
        await state.finish()
        await interface_all_begin2(call, state)
    else:
        pass
    


async def deactivete(call: types.CallbackQuery):
    Title_Test_code = BotDB.get_test_title_code_test(call.from_user.id, True)
    button =  InlineKeyboardMarkup()
    all1 = "Тесты доступные для отключения\n"
    for a in Title_Test_code:
        all1 = all1 + "\n" + "Код теста: " + a[1] + "\n" + "Название теста: " + a[0]
        button_h = types.InlineKeyboardButton((a[1]), callback_data = a[1])
        button.add(button_h)
    button_h = types.InlineKeyboardButton(("Отмена"), callback_data = "start")
    button.add(button_h)
    await call.message.answer(all1, reply_markup = button)
    await all.test_activateQ2.set()


async def deactivete2(call: types.CallbackQuery, state: FSMContext):
    flag = 0
    Title_Test_code = BotDB.get_test_title_code_test(call.from_user.id, True)
    for a in Title_Test_code:
        if a[1] == str(call.data):
            flag = 1
    if flag == 1:
        BotDB.test_update_active_mode(call.data, False)
        await call.message.answer("Тест с кодом " + str(call.data) + " отключен")
        await state.finish()
        await interface_all_begin2(call, state)
    else:
        pass


def register_activete(dp: Dispatcher):
    dp.register_callback_query_handler(activete, lambda c: c.data == "activete", state=all.interface_all_stateQ1)
    dp.register_callback_query_handler(activete2, state=all.test_activateQ1)
    dp.register_callback_query_handler(deactivete, lambda c: c.data == "deactivete", state=all.interface_all_stateQ1)
    dp.register_callback_query_handler(deactivete2, state=all.test_activateQ2)