from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardMarkup
from tgbot.misc.states import all
from tgbot.middlewares.DBhelp import BotDB
   
number_of_changes_rename = 1  #количесто попыток изменения имени


async def interface_all_begin(message: types.Message, state: FSMContext):
    await state.finish()
    button =  InlineKeyboardMarkup()
    if BotDB.get_teachers_name(message.from_user.id) != None:
        button_h = types.InlineKeyboardButton(text="Пройти тест", callback_data="test")
        button.add(button_h)
        button_h = types.InlineKeyboardButton(text="Управление тестом", callback_data="create")
        button.add(button_h)
        button_h = types.InlineKeyboardButton(text="Добавить преподавателя", callback_data="registration_teachers")
        button.add(button_h)
        await all.interface_all_stateBegin.set()
    else:
        if BotDB.user_exists(message.from_user.id) != None:
            button_h = types.InlineKeyboardButton(text="Начать тест", callback_data="passing_the_test")
            button.add(button_h)
            num = BotDB.get_test_user_rename_number_of_changes(message.from_user.id)
            if num[0] < number_of_changes_rename:
                button_h = types.InlineKeyboardButton(text="Изменить имя", callback_data="rename")
                button.add(button_h)
        else:
            button_h = types.InlineKeyboardButton(text="Регистрация", callback_data="registration")
            button.add(button_h) 
    await message.answer("Выберите вариант",reply_markup = button)
   

async def interface_all_begin2(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    button =  InlineKeyboardMarkup()
    if BotDB.get_teachers_name(call.from_user.id) != None:
        button_h = types.InlineKeyboardButton(text="Пройти тест", callback_data="test")
        button.add(button_h)
        button_h = types.InlineKeyboardButton(text="Управление тестом", callback_data="create")
        button.add(button_h)
        button_h = types.InlineKeyboardButton(text="Добавить преподавателя", callback_data="registration_teachers")
        button.add(button_h)
        await all.interface_all_stateBegin.set()
    else:
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
    await call.message.answer("Выберите вариант",reply_markup = button)
    await all.interface_all_stateBegin.set()



async def interface_all_begin3(message: types.Message, state: FSMContext):
    await interface_all_begin(message, state)



async def interface_all_begin4(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    button =  InlineKeyboardMarkup()
    if BotDB.get_teachers_name(call.chat.id) != None:
        button_h = types.InlineKeyboardButton(text="Пройти тест", callback_data="test")
        button.add(button_h)
        button_h = types.InlineKeyboardButton(text="Управление тестом", callback_data="create")
        button.add(button_h)
        button_h = types.InlineKeyboardButton(text="Добавить преподавателя", callback_data="registration_teachers")
        button.add(button_h)
        await all.interface_all_stateBegin.set()
    else:
        if BotDB.user_exists(call.chat.id) != None:
            button_h = types.InlineKeyboardButton(text="Начать тест", callback_data="passing_the_test")
            button.add(button_h)
            num = BotDB.get_test_user_rename_number_of_changes(call.chat.id)
            if num[0] < number_of_changes_rename:
                button_h = types.InlineKeyboardButton(text="Изменить имя", callback_data="rename")
                button.add(button_h)
        else:
            button_h = types.InlineKeyboardButton(text="Регистрация", callback_data="registration")
            button.add(button_h)
    await call.answer("Выберите вариант",reply_markup = button)
    await all.interface_all_stateBegin.set()


    
async def interface_all_passing_the_test(call: types.CallbackQuery, state: FSMContext):
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
    await state.finish()

        


async def interface_all_test_create(call: types.CallbackQuery, state: FSMContext):
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
    button_h = types.InlineKeyboardButton(text="Удалить тест", callback_data="test_del")
    button.add(button_h)
    button_h = types.InlineKeyboardButton(text="Назад", callback_data="start")
    button.add(button_h)
    await call.message.answer("Выберите вариант",reply_markup = button)
    await state.finish()




def register_interface_all(dp: Dispatcher):
    all2 = all,None
    dp.register_callback_query_handler(interface_all_begin2,lambda c: c.data == "start", state=all2)
    dp.register_message_handler(interface_all_begin,content_types = ['text'], state=all2)
    dp.register_message_handler(interface_all_begin3,commands=["start"], state=all2)
    dp.register_callback_query_handler(interface_all_passing_the_test,lambda c: c.data == "test", state=all.interface_all_stateBegin)
    dp.register_callback_query_handler(interface_all_test_create,lambda c: c.data == "create", state=all.interface_all_stateBegin)