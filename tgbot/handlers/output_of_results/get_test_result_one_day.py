from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
import asyncio
import datetime
from aiogram.utils.keyboard import InlineKeyboardBuilder
from tgbot.middlewares.DBhelp import BotDB
from tgbot.misc.states import all
from tgbot.misc.deleting_last_messages import deleting_last_messages
#ошибки 4000
    
    

router = Router()

@router.callback_query(F.data == "get_test_result_one_day", all.interface_all_stateQ1)
async def get_test_result_one_day(call: types.CallbackQuery, state: FSMContext):
    try:
        Title_Test_code = BotDB.get_test_title_test_code_no_active_mode(call.from_user.id)
        keyboard =  InlineKeyboardBuilder()
        all1 = "Тесты, данные о которых вы можете получить\n"
        for a in Title_Test_code:
            all1 = all1 + "\n" + "Код теста: " + a[1] + "\n" + "Название теста: " + a[0]
            button_h = types.InlineKeyboardButton(text = a[1], callback_data = a[1])
            keyboard.row(button_h)
        button_h = types.InlineKeyboardButton(text = "Отмена", callback_data = "start")
        keyboard.row(button_h)
        await deleting_last_messages(state)
        last_message = await call.message.answer(all1, reply_markup = keyboard.as_markup())
        await state.update_data(last_message=last_message)
        await state.set_state(state=all.register_get_test_result_one_dayQ1)
    except:
        await call.message.answer("Произошла ошибка 4001")
        await state.clear()

@router.callback_query(all.register_get_test_result_one_dayQ1)
async def get_test_result_one_day2(call: types.CallbackQuery, state: FSMContext):
    try:
        flag = 0
        Title_Test_code = BotDB.get_test_title_test_code_no_active_mode(call.from_user.id)
        for a in Title_Test_code:
            if a[1] == str(call.data):
                flag = 1
        if flag == 1:
            await state.update_data(test_code=call.data)
            test_id = BotDB.get_test_user_create_id(int(call.from_user.id), str(call.data))
            res = BotDB.get_test_result_all(test_id[0][0])
            data_2 = datetime.datetime.now()
            message_id_list = []
            message_id_list_deleting_last_messages = []
            for r in res:
                data = datetime.datetime.strptime(r[3], '%Y-%m-%d %H:%M:%S')
                data_3 = data_2 - data
                if data_3.days < 10:
                    text = ""
                    user_id = r[0]
                    user_date = BotDB.get_user(user_id)
                    text = text + "Группа: " + user_date[1] + "\n"
                    text = text + "Фамилия Имя: " + user_date[0] + "\n"
                    if r[1] != None:
                        text = text + "Количество верных ответов/общее количество ответов: " + r[1] + "\n"
                        text = text + "Оценка: " + str(r[2])
                    else:
                        text = text + "В данный момент проходит тест"
                    keyboard =  InlineKeyboardBuilder()
                    button_h = types.InlineKeyboardButton(text="Удалить", callback_data=str(r[4]))
                    keyboard.row(button_h)
                    message_id = await call.message.answer(text, reply_markup = keyboard.as_markup())
                    message_id_list_deleting_last_messages.append(message_id)
                    message_id_list.append([str(r[4]),message_id])
            await state.update_data(message_id=message_id_list)
            keyboard =  InlineKeyboardBuilder()
            button_h = types.InlineKeyboardButton(text="Назад", callback_data="start")
            keyboard.row(button_h)
            await deleting_last_messages(state)
            last_message = await call.message.answer("Выберите вариант", reply_markup = keyboard.as_markup())
            await state.update_data(last_message=message_id_list_deleting_last_messages.append(last_message))
            await state.set_state(state=all.register_get_test_result_one_dayQ2)
        else:
            pass
    except:
        await call.message.answer("Произошла ошибка 4002")
        await state.clear()

    
@router.callback_query(all.register_get_test_result_one_dayQ2)
async def get_test_result_one_day3(call: types.CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        call_data = data["test_code"]
        test_id = BotDB.get_test_user_create_id(int(call.from_user.id), str(call_data))
        res = BotDB.get_test_result_all(test_id[0][0])
        flag = 0
        for a in res:
            if a[4] == int(call.data):
                flag = 1
        if flag == 1:
            BotDB.test_result_del(call.data)
            data = await state.get_data()
            for d in data["message_id"]:
                if d[0] == call.data:
                    message_id = d[1]
            try:
                asyncio.create_task(await message_id.delete())
            except:
                pass
        else:
            pass
    except:
        await call.message.answer("Произошла ошибка 4003")
        await state.clear()