from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram import Router, F
from aiogram.filters import Command
from tgbot.middlewares.DBhelp import BotDB
from tgbot.misc.states import all, test_status, registration_teachers_status, rename_state, reg_us
from tgbot.handlers.interface_all import interface_all_begin2, interface_all_begin
import datetime
import random
import string
#ошибки 9100
length = 20     #длинна пароля


router = Router()


@router.callback_query(F.data == "registration_teachers", all.interface_all_stateBegin)
async def registration_teachers(call: types.CallbackQuery, state: FSMContext):
    try:
        result = 1
        while result != None:
            letters = string.ascii_uppercase
            password = ''.join(random.choice(letters) for i in range(length))
            result = BotDB.get_teachers_password(password)
        time = datetime.datetime.now()
        BotDB.teachers_password_add(password, time, call.from_user.id)
        await call.message.answer("Пароль: " + password + "\nДействителен 1 день с этого момента")
        await call.message.answer("Для регистрации необходимо ввести /registration")
        await interface_all_begin2(call, state)
    except:
        await call.message.answer("Произошла ошибка 9101")
        await state.clear()
    


@router.message(F.text, Command("registration"), default_state)
@router.message(F.text, Command("registration"), all.interface_all_stateBegin)
@router.message(F.text, Command("registration"), all.interface_all_stateQ1)
@router.message(F.text, Command("registration"), all.test_readQ1)
@router.message(F.text, Command("registration"), all.get_testQ1)
@router.message(F.text, Command("registration"), all.test_picturesQ1)
@router.message(F.text, Command("registration"), all.test_pictures_delQ1)
@router.message(F.text, Command("registration"), all.test_del_stateQ1)
@router.message(F.text, Command("registration"), all.test_del_stateQ2)
@router.message(F.text, Command("registration"), all.test_activateQ1)
@router.message(F.text, Command("registration"), all.test_activateQ2)
@router.message(F.text, Command("registration"), all.register_get_test_result_one_dayQ1)
@router.message(F.text, Command("registration"), all.register_get_test_result_one_dayQ2)
@router.message(F.text, Command("registration"), all.get_test_adminQ1)
@router.message(F.text, Command("registration"), test_status.Q1)
@router.message(F.text, Command("registration"), test_status.Q2)
@router.message(F.text, Command("registration"), rename_state.Q1)
@router.message(F.text, Command("registration"), rename_state.Q2)
@router.message(F.text, Command("registration"), reg_us.Q1)
async def registration_teachers2(message: types.Message, state: FSMContext):
    try:
        a = BotDB.get_teachers_name(message.from_user.id)
        if (a != None):
            await message.answer("Вы уже зарегествированны")
            await state.clear()    
        else:
            await message.answer("Введите пароль")
            await state.set_state(state= registration_teachers_status.Q1)
    except:
        await message.answer("Произошла ошибка 9102")
        await state.clear()

@router.message(F.text, registration_teachers_status.Q1)
async def registration_teachers3(message: types.Message, state: FSMContext):
    try:
        a = BotDB.get_teachers_password(message.text)
        if(a == None):
            await message.answer("Неверный пароль")
            await state.clear()
        else:
            data = BotDB.get_teachers_data(a[0])
            data_2 = datetime.datetime.now()
            data_3 = datetime.datetime.strptime(data[0], '%Y-%m-%d %H:%M:%S.%f')
            data_4 = data_2 - data_3
            if int(data_4.days) == 0:
                await message.answer("Пароль верный\nДля регистрации введите ФИО")
                await state.update_data(id=a[0])
                await state.set_state(state= registration_teachers_status.Q2)
            else:
                await message.answer("Неверный пароль")
                user_id = BotDB.get_teachers_user_id(a[0])
                BotDB.teachers_password_add(0, 0, user_id[0])
                await state.clear()
    except:
        await message.answer("Произошла ошибка 9103")
        await state.clear()


@router.message(F.text, registration_teachers_status.Q2)
async def registration_teachers4(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        id = data['id'] 
        BotDB.teachers_add(message.text, message.from_user.id, id)
        await state.clear()
        await message.answer("Регистрация завершена")
        interface_all_begin(message, state)
    except:
        await message.answer("Произошла ошибка 9104")
        await state.clear()
