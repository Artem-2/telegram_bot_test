from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from tgbot.middlewares.DBhelp import BotDB
from tgbot.misc.states import all,reg_us
from tgbot.handlers.interface_all import interface_all_begin
from aiogram.types import InlineKeyboardMarkup
#ошибки 9000



async def Registration(call: types.CallbackQuery, state: FSMContext):
    try:
        button =  InlineKeyboardMarkup()
        button_h = types.InlineKeyboardButton(text="Отмена", callback_data="start")
        button.add(button_h)
        await call.message.answer("Введите имя, фамилию (пример: Иванов Иван)", reply_markup = button)
        await reg_us.Q1.set()
    except:
        await call.message.answer("Произошла ошибка 9001")
        await state.finish()


    
async def Registration2(message: types.Message, state: FSMContext):
    try:
        answer = message.text
        async with state.proxy() as data:
            data["answer1"] = answer
        await message.answer("Введите группу (пример: 19-В-1)")
        await reg_us.Q2.set()
    except:
        await message.answer("Произошла ошибка 9002")
        await state.finish()


async def Registration3(message: types.Message, state: FSMContext):
    try:
        answer = message.text
        async with state.proxy() as data:
            data["answer2"] = answer
        BotDB.user_add(message.from_user.id, data["answer1"], data["answer2"])
        await message.answer("Регистрация завершена")
        await message.answer(data["answer1"])
        await message.answer(data["answer2"])
        await state.finish()
        await interface_all_begin(message, state)
    except:
        await message.answer("Произошла ошибка 9003")
        await state.finish()

    




def register_Registration(dp: Dispatcher):
    dp.register_callback_query_handler(Registration, lambda c: c.data == "registration", state=all.interface_all_stateQ1)
    dp.register_message_handler(Registration2, content_types = ['text'], state=reg_us.Q1)
    dp.register_message_handler(Registration3, content_types = ['text'], state=reg_us.Q2)