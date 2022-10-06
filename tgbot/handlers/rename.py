from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup
from tgbot.middlewares.DBhelp import BotDB
from tgbot.misc.states import all, rename_state
from tgbot.handlers.interface_all import interface_all_begin
#ошибки 9200



async def rename0(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.answer("Изменение имени доступно 1 раз")
        button =  InlineKeyboardMarkup()
        button_h = types.InlineKeyboardButton(text="Начать", callback_data="begin_rename")
        button.add(button_h)
        button_h = types.InlineKeyboardButton(text="Отмена", callback_data="start")
        button.add(button_h)
        await call.message.answer("Выберите вариант",reply_markup = button)
        await rename_state.Q1.set()
    except:
        await call.message.answer("Произошла ошибка 9201")
        await state.finish()

async def rename1(call: types.CallbackQuery, state: FSMContext):
    try:
        if call.data == "begin_rename":
            await call.message.answer("Введите имя, фамилию (пример: Иванов Иван)")
            await rename_state.Q2.set()
        else:
            pass
    except:
        await call.message.answer("Произошла ошибка 9202")
        await state.finish()


    
async def rename2(message: types.Message, state: FSMContext):
    try:
        answer = message.text

        async with state.proxy() as data:
            data["answer1"] = answer
        
        await message.answer("Введите группу (пример: 19-В-1)")
        await rename_state.Q3.set()
    except:
        await message.answer("Произошла ошибка 9203")
        await state.finish()





async def rename3(message: types.Message, state: FSMContext):
    try:
        answer = message.text

        async with state.proxy() as data:
            data["answer2"] = answer
    
        i = BotDB.get_test_user_rename_number_of_changes(message.from_user.id)
        i1 = i[0] + 1
        BotDB.test_user_rename(data["answer1"], data["answer2"], i1, message.from_user.id)
        await message.answer("Изменение регестрации завершено")
        await message.answer(data["answer1"])
        await message.answer(data["answer2"])
        await state.finish()
        await interface_all_begin(message, state)
    except:
        await message.answer("Произошла ошибка 9204")
        await state.finish()

    




def register_user_rename(dp: Dispatcher):
    dp.register_callback_query_handler(rename0, lambda c: c.data == "rename", state = all.interface_all_stateQ1)
    dp.register_callback_query_handler(rename1, lambda c: c.data == "begin_rename", state=rename_state.Q1)
    dp.register_message_handler(rename2, content_types = ['text'], state=rename_state.Q2)
    dp.register_message_handler(rename3, content_types = ['text'], state=rename_state.Q3)