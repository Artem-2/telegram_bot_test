from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardMarkup
from tgbot.misc.states import interface_all_state
from tgbot.middlewares.DBhelp import BotDB
   
number_of_changes_rename = 1  #количесто попыток изменения имени


async def interface_all_begin(message: types.Message, state: FSMContext):
    await state.finish()
    button =  InlineKeyboardMarkup()
    button_h = types.InlineKeyboardButton(text="Пройти тест", callback_data="test")
    button.add(button_h)
    if BotDB.get_teachers_name(message.from_user.id) != None:
        button_h = types.InlineKeyboardButton(text="Создать тест", callback_data="create")
        button.add(button_h)
        button_h = types.InlineKeyboardButton(text="Добавить преподавателя", callback_data="registration_teachers")
        button.add(button_h)
    await message.answer("Выберите вариант",reply_markup = button)
    await interface_all_state.Begin.set()

async def interface_all_begin2(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    button =  InlineKeyboardMarkup()
    button_h = types.InlineKeyboardButton(text="Пройти тест", callback_data="test")
    button.add(button_h)
    if BotDB.get_teachers_name(call.from_user.id)!= None:
        button_h = types.InlineKeyboardButton(text="Создать тест", callback_data="create")
        button.add(button_h)
        button_h = types.InlineKeyboardButton(text="Добавить преподавателя", callback_data="registration_teachers")
        button.add(button_h)
    await call.message.answer("Выберите вариант",reply_markup = button)
    await interface_all_state.Begin.set()

async def interface_all_begin3(message: types.Message, state: FSMContext):
    await state.finish()
    button =  InlineKeyboardMarkup()
    button_h = types.InlineKeyboardButton(text="Пройти тест", callback_data="test")
    button.add(button_h)
    if BotDB.get_teachers_name(message.from_user.id) != None:
        button_h = types.InlineKeyboardButton(text="Создать тест", callback_data="create")
        button.add(button_h)
        button_h = types.InlineKeyboardButton(text="Добавить преподавателя", callback_data="registration_teachers")
        button.add(button_h)
    await message.answer("Выберите вариант",reply_markup = button)
    await interface_all_state.Begin.set()

    
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
    dp.register_callback_query_handler(interface_all_begin2,lambda c: c.data == "start", state="*")
    dp.register_message_handler(interface_all_begin,content_types = ['text'], state=None)
    dp.register_message_handler(interface_all_begin3,commands=["start"], state="*")
    dp.register_callback_query_handler(interface_all_passing_the_test,lambda c: c.data == "test", state=interface_all_state.Begin)
    dp.register_callback_query_handler(interface_all_test_create,lambda c: c.data == "create", state=interface_all_state.Begin)