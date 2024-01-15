from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram import Router, F

from aiogram.utils.keyboard import InlineKeyboardBuilder
from tgbot.middlewares.DBhelp import BotDB
from tgbot.misc.states import all
from tgbot.handlers.interface_all import interface_all_begin2
#Ошибки 1000
    

router = Router()

@router.callback_query(F.data == "activete", all.interface_all_stateQ1)
async def activete(call: types.CallbackQuery, state: FSMContext):
    try:
        Title_Test_code = BotDB.get_test_title_code_test(call.from_user.id, False)
        keyboard =  InlineKeyboardBuilder()
        all1 = "Тесты доступные для активации\n"
        for a in Title_Test_code:
            all1 = all1 + "\n" + "Код теста: " + a[1] + "\n" + "Название теста: " + a[0]
            button_h = types.InlineKeyboardButton(text=a[1], callback_data = a[1])
            keyboard.row(button_h)
        button_h = types.InlineKeyboardButton(text="Отмена", callback_data = "start")
        keyboard.row(button_h)
        await call.message.answer(all1, reply_markup = keyboard.as_markup())
        await state.set_state(state=all.test_activateQ1)
    except:
        await call.message.answer("Произошла ошибка 1001")
        await state.clear()


@router.callback_query(all.test_activateQ1)
async def activete2(call: types.CallbackQuery, state: FSMContext):
    try:
        flag = 0
        Title_Test_code = BotDB.get_test_title_code_test(call.from_user.id, False)
        for a in Title_Test_code:
            if a[1] == str(call.data):
                flag = 1
        if flag == 1:
            BotDB.test_update_active_mode(call.data, True)
            await call.message.answer("Тест с кодом " + str(call.data) + " активирован")
            await state.clear()
            await interface_all_begin2(call, state)
        else:
            pass
    except:
        await call.message.answer("Произошла ошибка 1002")
        await state.clear()
    


@router.callback_query(F.data == "deactivete", all.interface_all_stateQ1)
async def deactivete(call: types.CallbackQuery, state: FSMContext):
    try:
        Title_Test_code = BotDB.get_test_title_code_test(call.from_user.id, True)
        keyboard =  InlineKeyboardBuilder()
        all1 = "Тесты доступные для отключения\n"
        for a in Title_Test_code:
            all1 = all1 + "\n" + "Код теста: " + a[1] + "\n" + "Название теста: " + a[0]
            button_h = types.InlineKeyboardButton(text=a[1], callback_data = a[1])
            keyboard.row(button_h)
        button_h = types.InlineKeyboardButton(text="Отмена", callback_data = "start")
        keyboard.row(button_h)
        await call.message.answer(all1, reply_markup = keyboard.as_markup())
        await state.set_state(state=all.test_activateQ2)
    except:
        await call.message.answer("Произошла ошибка 1003")
        await state.clear()


@router.callback_query(all.test_activateQ2)
async def deactivete2(call: types.CallbackQuery, state: FSMContext):
    try:
        flag = 0
        Title_Test_code = BotDB.get_test_title_code_test(call.from_user.id, True)
        for a in Title_Test_code:
            if a[1] == str(call.data):
                flag = 1
        if flag == 1:
            BotDB.test_update_active_mode(call.data, False)
            await call.message.answer("Тест с кодом " + str(call.data) + " отключен")
            await state.clear()
            await interface_all_begin2(call, state)
        else:
            pass
    except:
        await call.message.answer("Произошла ошибка 1004")
        await state.clear()