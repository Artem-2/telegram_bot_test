from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, F
from tgbot.middlewares.DBhelp import BotDB
from tgbot.misc.states import all
from tgbot.handlers.interface_all import interface_all_begin2
from tgbot.misc.deleting_last_messages import deleting_last_messages
#ошибки 9400


router = Router()



@router.callback_query(F.data == "test_del", all.interface_all_stateQ1)
async def test_del1(call: types.CallbackQuery, state: FSMContext):
    try:
        Title_Test_code = BotDB.get_test_title_test_code_no_active_mode(call.from_user.id)
        keyboard =  InlineKeyboardBuilder()
        all1 = "Тесты которыe вы можете удалить:\n"
        for a in Title_Test_code:
            all1 = all1 + "\n" + "Код теста: " + a[1] + "\n" + "Название теста: " + a[0]
            button_h = types.InlineKeyboardButton(text = a[1], callback_data = a[1])
            keyboard.row(button_h)
        button_h = types.InlineKeyboardButton(text = "Отмена", callback_data = "start")
        keyboard.row(button_h)
        await deleting_last_messages(state)
        last_message = await call.message.answer(all1, reply_markup = keyboard.as_markup())
        await state.update_data(last_message=last_message)
        await state.set_state(state= all.test_del_stateQ1)
    except:
        await call.message.answer("Произошла ошибка 9401")
        await state.clear()



@router.callback_query(all.test_del_stateQ1)
async def test_del2(call: types.CallbackQuery, state: FSMContext):
    try:
        flag = 0
        Title_Test_code = BotDB.get_test_title_test_code_no_active_mode(call.from_user.id)
        for a in Title_Test_code:
            if a[1] == str(call.data):
                flag = 1
        if flag == 1:
            a = BotDB.get_test_user_create_id(int(call.from_user.id), str(call.data))
            await state.update_data(test_id_del=a[0][0])
            keyboard =  InlineKeyboardBuilder()
            button_h = types.InlineKeyboardButton(text = "Продолжить", callback_data = "test_del_activate")
            keyboard.row(button_h)
            button_h = types.InlineKeyboardButton(text = "Отмена", callback_data = "start")
            keyboard.row(button_h)
            await deleting_last_messages(state)
            last_message = await call.message.answer("Код теста который будет удален: " + str(call.data), reply_markup = keyboard.as_markup())
            await state.update_data(last_message=last_message)
            await state.set_state(state= all.test_del_stateQ2)
        else:
            pass
    except:
        await call.message.answer("Произошла ошибка 9402")
        await state.clear()


@router.callback_query(F.data == "test_del_activate", all.test_del_stateQ2)
async def test_del3(call: types.CallbackQuery, state: FSMContext):
    try:
        if call.data == "test_del_activate":
            data = await state.get_data()
            a = data["test_id_del"]
            BotDB.test_del(a)
            await deleting_last_messages(state)
            await call.message.answer("Тест удален")
            await state.clear()
            await interface_all_begin2(call, state)
        else:
            pass
    except:
        await call.message.answer("Произошла ошибка 9403")
        await state.clear()
