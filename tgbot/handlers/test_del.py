from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup
from tgbot.middlewares.DBhelp import BotDB
from tgbot.misc.states import test_del_state
from tgbot.handlers.interface_all import interface_all_begin2
    





async def test_del1(call: types.CallbackQuery):
    Title_Test_code = BotDB.get_test_title_test_code_no_active_mode(call.from_user.id)
    button =  InlineKeyboardMarkup()
    all = "Тесты которыe вы можете удалить\n"
    for a in Title_Test_code:
        all = all + "\n" + "Код теста: " + a[1] + "\n" + "Название теста: " + a[0]
        button_h = types.InlineKeyboardButton((a[1]), callback_data = a[1])
        button.add(button_h)
    button_h = types.InlineKeyboardButton(("Отмена"), callback_data = "start")
    button.add(button_h)
    await call.message.answer(all, reply_markup = button)
    await call.message.answer("Введите код теста который вы хотите удалить")
    await test_del_state.Q1.set()



async def test_del2(call: types.CallbackQuery, state: FSMContext):
    a = BotDB.get_test_user_create_id(int(call.from_user.id), str(call.data))
    async with state.proxy() as data:
        data["test_id_del"] = a[0][0]
    button =  InlineKeyboardMarkup()
    button_h = types.InlineKeyboardButton(("Продолжить"), callback_data = "test_del_activate")
    button.add(button_h)
    button_h = types.InlineKeyboardButton(("Отмена"), callback_data = "start")
    button.add(button_h)
    await call.message.answer("Код теста который будет удален " + str(call.data), reply_markup = button)
    await test_del_state.Q2.set()


async def test_del3(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        a = data["test_id_del"]
    BotDB.test_del(a)
    await call.message.answer("Тест удален")
    await state.finish()
    await interface_all_begin2(call, state)




def register_test_del(dp: Dispatcher):
    dp.register_callback_query_handler(test_del1,lambda c: c.data == "test_del", state=None)
    dp.register_callback_query_handler(test_del2, state=test_del_state.Q1)
    dp.register_callback_query_handler(test_del3, lambda c: c.data == "test_del_activate", state=test_del_state.Q2)