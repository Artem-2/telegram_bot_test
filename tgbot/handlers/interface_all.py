from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardMarkup
from tgbot.misc.states import all, test_status, rename_state, reg_us
from tgbot.middlewares.DBhelp import BotDB
#ошибки 5000
number_of_changes_rename = 1  #количесто попыток изменения имени

async def interface_all_begin_def(message_id, message: types.Message, state: FSMContext):
    try:
        await state.finish()
        button =  InlineKeyboardMarkup()
        if BotDB.get_teachers_name(message_id) != None:
            button_h = types.InlineKeyboardButton(text="Пройти тест", callback_data="test")
            button.add(button_h)
            button_h = types.InlineKeyboardButton(text="Управление тестом", callback_data="create")
            button.add(button_h)
            button_h = types.InlineKeyboardButton(text="Добавить преподавателя", callback_data="registration_teachers")
            button.add(button_h)
            await all.interface_all_stateBegin.set()
            await message.answer("Выберите вариант",reply_markup = button)
        else:
            if BotDB.user_exists(message_id) != None:
                button_h = types.InlineKeyboardButton(text="Начать тест", callback_data="passing_the_test")
                button.add(button_h)
                num = BotDB.get_test_user_rename_number_of_changes(message_id)
                if num[0] < number_of_changes_rename:
                    button_h = types.InlineKeyboardButton(text="Изменить имя", callback_data="rename")
                    button.add(button_h)
                await message.answer("Выберите вариант",reply_markup = button)
            else:
                button_h = types.InlineKeyboardButton(text="Регистрация", callback_data="registration")
                button.add(button_h) 
                await message.answer("Необходимо пройти регистрацию",reply_markup = button)
            await all.interface_all_stateQ1.set()
    except:
        await message.answer("Произошла ошибка 5001")
        await state.finish()


async def interface_all_begin(message: types.Message, state: FSMContext):
    await interface_all_begin_def(message.from_user.id, message, state)

async def interface_all_begin2(call: types.CallbackQuery, state: FSMContext):
    await interface_all_begin_def(call.from_user.id, call.message, state)

async def interface_all_begin3(message: types.Message, state: FSMContext):
    await interface_all_begin(message, state)

async def interface_all_begin4(call: types.CallbackQuery, state: FSMContext):
    await interface_all_begin_def(call.chat.id, call, state)


    
async def interface_all_passing_the_test(call: types.CallbackQuery, state: FSMContext):
    try:
        button =  InlineKeyboardMarkup()
        if BotDB.user_exists(call.from_user.id) != None:
            button_h = types.InlineKeyboardButton(text="Начать тест", callback_data="passing_the_test")
            button.add(button_h)
            num = BotDB.get_test_user_rename_number_of_changes(call.from_user.id)
            if num[0] < number_of_changes_rename:
                button_h = types.InlineKeyboardButton(text="Изменить имя", callback_data="rename")
                button.add(button_h)
        else:
            button_h = types.InlineKeyboardButton(text="Регистрация", callback_data="registration")
            button.add(button_h)
        button_h = types.InlineKeyboardButton(text="Назад", callback_data="start")
        button.add(button_h)
        await call.message.answer("Выберите вариант",reply_markup = button)
        await all.interface_all_stateQ1.set()
    except:
        await call.message.answer("Произошла ошибка 5002")
        await state.finish()

        


async def interface_all_test_create(call: types.CallbackQuery, state: FSMContext):
    try:
        button =  InlineKeyboardMarkup()
        button_h = types.InlineKeyboardButton(text="Создать тест", callback_data="test_create")
        button.add(button_h)
        button_h = types.InlineKeyboardButton(text="Добавить картинку", callback_data="pictures")
        button.add(button_h)
        button_h = types.InlineKeyboardButton(text="Удалить картинку", callback_data="pictures_del")
        button.add(button_h)
        button_h = types.InlineKeyboardButton(text="Помощь в создании теста", callback_data="test_create_help")
        button.add(button_h)
        button_h = types.InlineKeyboardButton(text="Активировать тест", callback_data="activete")
        button.add(button_h)
        button_h = types.InlineKeyboardButton(text="Отключить тест", callback_data="deactivete")
        button.add(button_h)
        button_h = types.InlineKeyboardButton(text="Результаты теста", callback_data="get_test_result")
        button.add(button_h)
        button_h = types.InlineKeyboardButton(text="Результаты теста за 1 день", callback_data="get_test_result_one_day")
        button.add(button_h)
        button_h = types.InlineKeyboardButton(text="Удалить тест", callback_data="test_del")
        button.add(button_h)
        button_h = types.InlineKeyboardButton(text="Назад", callback_data="start")
        button.add(button_h)
        await call.message.answer("Выберите вариант",reply_markup = button)
        await all.interface_all_stateQ1.set()
    except:
        await call.message.answer("Произошла ошибка 5003")
        await state.finish()

            


async def interface_all_test_create_admin(message: types.Message, state: FSMContext):
    try:
        button =  InlineKeyboardMarkup()
        button_h = types.InlineKeyboardButton(text="Результаты теста (все)", callback_data="get_test_result_admin")
        button.add(button_h)
        button_h = types.InlineKeyboardButton(text="Отмена", callback_data="start")
        button.add(button_h)
        await message.answer("Выберите вариант",reply_markup = button)
        await all.interface_all_stateQ1.set()
    except:
        await message.answer("Произошла ошибка 5004")
        await state.finish()


def register_interface_all(dp: Dispatcher):
    all2 = all,None,test_status.Q1,test_status.Q2,rename_state.Q1,rename_state.Q2,reg_us.Q1
    dp.register_message_handler(interface_all_begin3,commands=["start"], state=all2)
    dp.register_message_handler(interface_all_test_create_admin,commands=["admin"], state=all2, is_admin=True)
    dp.register_message_handler(interface_all_begin,content_types = ['text'], state=all2)
    dp.register_callback_query_handler(interface_all_begin2,lambda c: c.data == "start", state=all2)
    dp.register_callback_query_handler(interface_all_passing_the_test,lambda c: c.data == "test", state=all.interface_all_stateBegin)
    dp.register_callback_query_handler(interface_all_test_create,lambda c: c.data == "create", state=all.interface_all_stateBegin)