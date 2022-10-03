from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from tgbot.middlewares.DBhelp import BotDB
from tgbot.misc.states import all
from tgbot.handlers.interface_all import interface_all_begin
from aiogram.types import InlineKeyboardMarkup




async def Registration(call: types.CallbackQuery):
    await call.message.answer("Введите имя, фамилию (пример: Иванов Иван)")
    button =  InlineKeyboardMarkup()
    button_h = types.InlineKeyboardButton(text="Отмена", callback_data="start")
    button.add(button_h)
    await all.reg_usQ1.set()


    
async def Registration2(message: types.Message, state: FSMContext):
    answer = message.text

    async with state.proxy() as data:
        data["answer1"] = answer
        
    await message.answer("Введите группу (пример: 19-В-1)")
    await all.reg_usQ2.set()


async def Registration3(message: types.Message, state: FSMContext):
    answer = message.text

    async with state.proxy() as data:
        data["answer2"] = answer
        
    BotDB.user_add(message.from_user.id, data["answer1"], data["answer2"])
    await message.answer("Регистрация завершена")
    await message.answer(data["answer1"])
    await message.answer(data["answer2"])
    await state.finish()
    await interface_all_begin(message, state)

    




def register_Registration(dp: Dispatcher):
    dp.register_callback_query_handler(Registration, lambda c: c.data == "registration")
    dp.register_message_handler(Registration2, content_types = ['text'], state=all.reg_usQ1)
    dp.register_message_handler(Registration3, content_types = ['text'], state=all.reg_usQ2)