from aiogram.fsm.context import FSMContext
from tgbot.misc.deleting_last_messages import deleting_last_messages
from aiogram import types
from tgbot.misc.states import all, test_status, rename_state, reg_us
from aiogram.fsm.state import default_state
from tgbot.middlewares.DBhelp import BotDB
from aiogram import Router, F
from aiogram.filters import Command

from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.filters.admin import AdminFilter
#ошибки 5000

from tgbot.misc.config import config
number_of_changes_rename = config.tg_bot.number_of_changes_rename  #количесто попыток изменения имени


all2 = all,default_state,test_status.Q1,test_status.Q2,rename_state.Q1,rename_state.Q2,reg_us.Q1

router = Router()


####################################################################################################################################################
@router.message(F.text, Command("admin"), default_state, AdminFilter(is_admin=True))
@router.message(F.text, Command("admin"), all.interface_all_stateBegin, AdminFilter(is_admin=True))
@router.message(F.text, Command("admin"), all.interface_all_stateQ1, AdminFilter(is_admin=True))
@router.message(F.text, Command("admin"), all.test_readQ1, AdminFilter(is_admin=True))
@router.message(F.text, Command("admin"), all.get_testQ1, AdminFilter(is_admin=True))
@router.message(F.text, Command("admin"), all.test_picturesQ1, AdminFilter(is_admin=True))
@router.message(F.text, Command("admin"), all.test_pictures_delQ1, AdminFilter(is_admin=True))
@router.message(F.text, Command("admin"), all.test_del_stateQ1, AdminFilter(is_admin=True))
@router.message(F.text, Command("admin"), all.test_del_stateQ2, AdminFilter(is_admin=True))
@router.message(F.text, Command("admin"), all.test_activateQ1, AdminFilter(is_admin=True))
@router.message(F.text, Command("admin"), all.test_activateQ2, AdminFilter(is_admin=True))
@router.message(F.text, Command("admin"), all.register_get_test_result_one_dayQ1, AdminFilter(is_admin=True))
@router.message(F.text, Command("admin"), all.register_get_test_result_one_dayQ2, AdminFilter(is_admin=True))
@router.message(F.text, Command("admin"), all.get_test_adminQ1, AdminFilter(is_admin=True))
@router.message(F.text, Command("admin"), test_status.Q1, AdminFilter(is_admin=True))
@router.message(F.text, Command("admin"), test_status.Q2, AdminFilter(is_admin=True))
@router.message(F.text, Command("admin"), rename_state.Q1, AdminFilter(is_admin=True))
@router.message(F.text, Command("admin"), rename_state.Q2, AdminFilter(is_admin=True))
@router.message(F.text, Command("admin"), reg_us.Q1, AdminFilter(is_admin=True))
async def interface_all_test_create_admin(message: types.Message, state: FSMContext):
    try:
        keyboard =  InlineKeyboardBuilder()
        button_h = types.InlineKeyboardButton(text="Результаты теста (все)", callback_data="get_test_result_admin")
        keyboard.row(button_h)
        button_h = types.InlineKeyboardButton(text="Отмена", callback_data="start")
        keyboard.row(button_h)
        await deleting_last_messages(state)
        last_message = await message.answer("Выберите вариант",reply_markup = keyboard.as_markup())
        await state.update_data(last_message=last_message)
        await state.set_state(state=all.interface_all_stateQ1)
    except:
        await message.answer("Произошла ошибка 5001")
        await state.clear()
####################################################################################################################################################
async def interface_all_begin_def(message_id, message: types.Message, state: FSMContext):
    try:
        keyboard =  InlineKeyboardBuilder()
        await deleting_last_messages(state)
        await state.clear()
        last_message = 0
        if BotDB.get_teachers_name(message_id) != None:
            button_h = types.InlineKeyboardButton(text="Пройти тест", callback_data="test")
            keyboard.row(button_h)
            button_h = types.InlineKeyboardButton(text="Управление тестом", callback_data="create")
            keyboard.row(button_h)
            button_h = types.InlineKeyboardButton(text="Добавить преподавателя", callback_data="registration_teachers")
            keyboard.row(button_h)
            await state.set_state(state=all.interface_all_stateBegin)
            last_message = await message.answer("Выберите вариант",reply_markup = keyboard.as_markup())
        else:
            if BotDB.user_exists(message_id) != None:
                button_h = types.InlineKeyboardButton(text="Начать тест", callback_data="passing_the_test_v2")
                keyboard.row(button_h)
                num = BotDB.get_test_user_rename_number_of_changes(message_id)
                if num[0] < number_of_changes_rename:
                    button_h = types.InlineKeyboardButton(text="Изменить имя", callback_data="rename")
                    keyboard.row(button_h)
                last_message = await message.answer("Выберите вариант",reply_markup = keyboard.as_markup())
            else:
                button_h = types.InlineKeyboardButton(text="Регистрация", callback_data="registration")
                keyboard.row(button_h) 
                last_message = await message.answer("Необходимо пройти регистрацию",reply_markup = keyboard.as_markup())
            await state.set_state(state=all.interface_all_stateQ1)
        await state.update_data(last_message=last_message)
    except:
        await message.answer("Произошла ошибка 5002")
        await state.clear()
####################################################################################################################################################
@router.callback_query(F.data == "start", default_state)
@router.callback_query(F.data == "start", all.interface_all_stateBegin)
@router.callback_query(F.data == "start", all.interface_all_stateQ1)
@router.callback_query(F.data == "start", all.test_readQ1)
@router.callback_query(F.data == "start", all.get_testQ1)
@router.callback_query(F.data == "start", all.test_picturesQ1)
@router.callback_query(F.data == "start", all.test_pictures_delQ1)
@router.callback_query(F.data == "start", all.test_del_stateQ1)
@router.callback_query(F.data == "start", all.test_del_stateQ2)
@router.callback_query(F.data == "start", all.test_activateQ1)
@router.callback_query(F.data == "start", all.test_activateQ2)
@router.callback_query(F.data == "start", all.register_get_test_result_one_dayQ1)
@router.callback_query(F.data == "start", all.register_get_test_result_one_dayQ2)
@router.callback_query(F.data == "start", all.get_test_adminQ1)
@router.callback_query(F.data == "start", test_status.Q1)
@router.callback_query(F.data == "start", test_status.Q2)
@router.callback_query(F.data == "start", rename_state.Q1)
@router.callback_query(F.data == "start", rename_state.Q2)
@router.callback_query(F.data == "start", reg_us.Q1)
async def interface_all_begin2(call: types.CallbackQuery, state: FSMContext):
    await interface_all_begin_def(call.from_user.id, call.message, state)
####################################################################################################################################################
@router.message(F.text, Command("start"), default_state)
@router.message(F.text, Command("start"), all.interface_all_stateBegin)
@router.message(F.text, Command("start"), all.interface_all_stateQ1)
@router.message(F.text, Command("start"), all.test_readQ1)
@router.message(F.text, Command("start"), all.get_testQ1)
@router.message(F.text, Command("start"), all.test_picturesQ1)
@router.message(F.text, Command("start"), all.test_pictures_delQ1)
@router.message(F.text, Command("start"), all.test_del_stateQ1)
@router.message(F.text, Command("start"), all.test_del_stateQ2)
@router.message(F.text, Command("start"), all.test_activateQ1)
@router.message(F.text, Command("start"), all.test_activateQ2)
@router.message(F.text, Command("start"), all.register_get_test_result_one_dayQ1)
@router.message(F.text, Command("start"), all.register_get_test_result_one_dayQ2)
@router.message(F.text, Command("start"), all.get_test_adminQ1)
@router.message(F.text, Command("start"), test_status.Q1)
@router.message(F.text, Command("start"), test_status.Q2)
@router.message(F.text, Command("start"), rename_state.Q1)
@router.message(F.text, Command("start"), rename_state.Q2)
@router.message(F.text, Command("start"), reg_us.Q1)
async def interface_all_begin3(message: types.Message, state: FSMContext):
    await interface_all_begin(message, state)
####################################################################################################################################################
async def interface_all_begin4(call: types.CallbackQuery, state: FSMContext):
    await interface_all_begin_def(call.chat.id, call, state)
####################################################################################################################################################
@router.callback_query(F.data == "test", all.interface_all_stateBegin)    
async def interface_all_passing_the_test(call: types.CallbackQuery, state: FSMContext):
    try:
        keyboard =  InlineKeyboardBuilder()
        if BotDB.user_exists(call.from_user.id) != None:
            button_h = types.InlineKeyboardButton(text="Начать тест", callback_data="passing_the_test_v2")
            keyboard.row(button_h)
            num = BotDB.get_test_user_rename_number_of_changes(call.from_user.id)
            if num[0] < number_of_changes_rename:
                button_h = types.InlineKeyboardButton(text="Изменить имя", callback_data="rename")
                keyboard.row(button_h)
        else:
            button_h = types.InlineKeyboardButton(text="Регистрация", callback_data="registration")
            keyboard.row(button_h)
        button_h = types.InlineKeyboardButton(text="Назад", callback_data="start")
        keyboard.row(button_h)
        await deleting_last_messages(state)
        last_message = await call.message.answer("Выберите вариант",reply_markup = keyboard.as_markup())
        await state.update_data(last_message=last_message)
        await state.set_state(state=all.interface_all_stateQ1)
    except:
        await call.message.answer("Произошла ошибка 5003")
        await state.clear()
####################################################################################################################################################
@router.callback_query(F.data == "create", all.interface_all_stateBegin)    
async def interface_all_test_create(call: types.CallbackQuery, state: FSMContext):
    try:
        keyboard =  InlineKeyboardBuilder()
        button_h = types.InlineKeyboardButton(text="Создать тест", callback_data="test_create")
        keyboard.row(button_h)
        button_h = types.InlineKeyboardButton(text="Добавить картинку", callback_data="pictures")
        keyboard.row(button_h)
        button_h = types.InlineKeyboardButton(text="Удалить картинку", callback_data="pictures_del")
        keyboard.row(button_h)
        button_h = types.InlineKeyboardButton(text="Помощь в создании теста", callback_data="test_create_help")
        keyboard.row(button_h)
        button_h = types.InlineKeyboardButton(text="Активировать тест", callback_data="activete")
        keyboard.row(button_h)
        button_h = types.InlineKeyboardButton(text="Отключить тест", callback_data="deactivete")
        keyboard.row(button_h)
        button_h = types.InlineKeyboardButton(text="Результаты теста", callback_data="get_test_result")
        keyboard.row(button_h)
        button_h = types.InlineKeyboardButton(text="Результаты теста за 1 день", callback_data="get_test_result_one_day")
        keyboard.row(button_h)
        button_h = types.InlineKeyboardButton(text="Удалить тест", callback_data="test_del")
        keyboard.row(button_h)
        button_h = types.InlineKeyboardButton(text="Назад", callback_data="start")
        keyboard.row(button_h)
        await deleting_last_messages(state)
        last_message = await call.message.answer("Выберите вариант",reply_markup = keyboard.as_markup())
        await state.update_data(last_message=last_message)
        await state.set_state(state=all.interface_all_stateQ1)
    except:
        await call.message.answer("Произошла ошибка 5004")
        await state.clear()
####################################################################################################################################################
@router.message(F.text, default_state)
@router.message(F.text, all.interface_all_stateBegin)
@router.message(F.text, all.interface_all_stateQ1)
@router.message(F.text, all.test_readQ1)
@router.message(F.text, all.get_testQ1)
@router.message(F.text, all.test_picturesQ1)
@router.message(F.text, all.test_pictures_delQ1)
@router.message(F.text, all.test_del_stateQ1)
@router.message(F.text, all.test_del_stateQ2)
@router.message(F.text, all.test_activateQ1)
@router.message(F.text, all.test_activateQ2)
@router.message(F.text, all.register_get_test_result_one_dayQ1)
@router.message(F.text, all.register_get_test_result_one_dayQ2)
@router.message(F.text, all.get_test_adminQ1)
@router.message(F.text, test_status.Q1)
@router.message(F.text, test_status.Q2)
@router.message(F.text, rename_state.Q1)
@router.message(F.text, rename_state.Q2)
@router.message(F.text, reg_us.Q1)
async def interface_all_begin(message: types.Message, state: FSMContext):
    await interface_all_begin_def(message.from_user.id, message, state)