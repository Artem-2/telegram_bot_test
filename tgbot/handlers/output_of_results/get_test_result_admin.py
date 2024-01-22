from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from tgbot.middlewares.DBhelp import BotDB
from tgbot.handlers.output_of_results.get_test_result import get_test_result2
from tgbot.misc.states import all
from aiogram.utils.keyboard import InlineKeyboardBuilder
#ошибки 3000

router = Router()


@router.callback_query(F.data == "get_test_result_admin", all.interface_all_stateQ1)
async def get_test_result_admin(call: types.CallbackQuery, state: FSMContext):
    try:
        Title_Test_code = BotDB.get_test_title_test_code_no_active_mode_admin()
        keyboard =  InlineKeyboardBuilder()
        all1 = "Тесты, данные о которых вы можете получить\n"
        for a in Title_Test_code:
            user_name = BotDB.get_teachers_name(a[2])
            all1 = all1 + "\nКод теста: " + a[1] + "\nНазвание теста: " + a[0] + "\nСоздатель: " + user_name[0] + "\n"
            button_h = types.InlineKeyboardButton(text=a[1], callback_data = a[1])
            keyboard.row(button_h)
        button_h = types.InlineKeyboardButton(text="Отмена", callback_data = "start")
        keyboard.row(button_h)
        await call.message.answer(all1, reply_markup = keyboard.as_markup())
        await state.set_state(state=all.get_test_adminQ1)
    except:
        await call.message.answer("Произошла ошибка 3001")
        await state.clear()

@router.callback_query(all.get_test_adminQ1)
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
        await state.clear()
