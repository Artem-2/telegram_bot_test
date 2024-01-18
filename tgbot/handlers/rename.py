from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, F
from tgbot.middlewares.DBhelp import BotDB
from tgbot.misc.states import all, rename_state
from tgbot.handlers.interface_all import interface_all_begin
#ошибки 9200

router = Router()


@router.callback_query(F.data == "rename", all.interface_all_stateQ1)
async def rename(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.answer("Изменение имени доступно 1 раз")
        keyboard =  InlineKeyboardBuilder()
        button_h = types.InlineKeyboardButton(text="Начать", callback_data="begin_rename")
        keyboard.row(button_h)
        button_h = types.InlineKeyboardButton(text="Отмена", callback_data="start")
        keyboard.row(button_h)
        await call.message.answer("Выберите вариант",reply_markup = keyboard.as_markup())
        await state.set_state(state= rename_state.Q1)
    except:
        await call.message.answer("Произошла ошибка 9201")
        await state.clear()

@router.callback_query(F.data == "begin_rename", rename_state.Q1)
async def rename1(call: types.CallbackQuery, state: FSMContext):
    try:
        if call.data == "begin_rename":
            keyboard =  InlineKeyboardBuilder()
            button_h = types.InlineKeyboardButton(text="Отмена", callback_data="start")
            keyboard.row(button_h)
            await call.message.answer("Введите фамилию", reply_markup = keyboard.as_markup())
            await state.set_state(state= rename_state.Q2)
        else:
            pass
    except:
        await call.message.answer("Произошла ошибка 9202")
        await state.clear()


@router.message(F.text, rename_state.Q2)
async def rename2(message: types.Message, state: FSMContext):
    try:
        surname = message.text
        await state.update_data(surname=surname)
        await message.answer("Введите имя")
        await state.set_state(state= rename_state.Q3)
    except:
        await message.answer("Произошла ошибка 9203")
        await state.clear()


@router.message(F.text, rename_state.Q3)
async def rename3(message: types.Message, state: FSMContext):
    try:
        name = message.text

        await state.update_data(name=name)
        
        await message.answer("Введите группу (пример: 19-В-1)")
        await state.set_state(state= rename_state.Q4)
    except:
        await message.answer("Произошла ошибка 9204")
        await state.clear()





@router.message(F.text, rename_state.Q4)
async def rename4(message: types.Message, state: FSMContext):
    try:
        group = message.text

        await state.update_data(group=group)
    
        data = await state.get_data()

        i = BotDB.get_test_user_rename_number_of_changes(message.from_user.id)
        i1 = i[0] + 1
        BotDB.test_user_rename(str(data["surname"]) + " " + str(data["name"]), data["group"], i1, message.from_user.id)
        await message.answer("Изменение регестрации завершено")
        await message.answer(str(data["surname"]) + " " + str(data["name"]))
        await message.answer(data["group"])
        await state.clear()
        await interface_all_begin(message, state)
    except:
        await message.answer("Произошла ошибка 9205")
        await state.clear()