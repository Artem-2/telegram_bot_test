from aiogram import types
from aiogram.fsm.context import FSMContext
from tgbot.middlewares.DBhelp import BotDB
from tgbot.misc.states import all,reg_us
from aiogram import Router, F
from tgbot.handlers.interface_all import interface_all_begin
from aiogram.utils.keyboard import InlineKeyboardBuilder
#ошибки 9000

router = Router()

@router.callback_query(F.data == "registration", all.interface_all_stateQ1)
async def Registration(call: types.CallbackQuery, state: FSMContext):
    try:
        keyboard =  InlineKeyboardBuilder()
        button_h = types.InlineKeyboardButton(text="Отмена", callback_data="start")
        keyboard.row(button_h)
        await call.message.answer("Введите фамилию", reply_markup = keyboard.as_markup())
        await state.set_state(state=reg_us.Q1)
    except:
        await call.message.answer("Произошла ошибка 9001")
        await state.clear()

@router.message(F.text, reg_us.Q1)
async def Registration1(message: types.Message, state: FSMContext):
    try:
        await state.update_data(surname=message.text)
        await message.answer("Введите имя")
        await state.set_state(state=reg_us.Q2)
    except:
        await message.answer("Произошла ошибка 9002")
        await state.clear()
    
@router.message(F.text, reg_us.Q2)
async def Registration2(message: types.Message, state: FSMContext):
    try:
        await state.update_data(name=message.text)
        await message.answer("Введите группу (пример: 19-В-1)")
        await state.set_state(state=reg_us.Q3)
    except:
        await message.answer("Произошла ошибка 9003")
        await state.clear()

@router.message(F.text, reg_us.Q3)
async def Registration3(message: types.Message, state: FSMContext):
    try:
        await state.update_data(group=message.text)
        data = await state.get_data()
        BotDB.user_add(message.from_user.id, str(data["surname"]) + " " + str(data["name"]), data["group"])
        await message.answer("Регистрация завершена")
        await message.answer(str(data["surname"]) + " " + str(data["name"]))
        await message.answer(data["group"])
        await state.clear()
        await interface_all_begin(message, state)
    except:
        await message.answer("Произошла ошибка 9004")
        await state.clear()
