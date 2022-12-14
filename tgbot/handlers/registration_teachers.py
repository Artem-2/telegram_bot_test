from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from tgbot.middlewares.DBhelp import BotDB
from tgbot.misc.states import all, test_status, registration_teachers_status, rename_state, reg_us
from tgbot.handlers.interface_all import interface_all_begin2, interface_all_begin
import datetime
import random
import string
#ошибки 9100
length = 20     #длинна пароля




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
        await state.finish()
    


async def registration_teachers2(message: types.Message, state: FSMContext):
    try:
        a = BotDB.get_teachers_name(message.from_user.id)
        if (a != None):
            await message.answer("Вы уже зарегествированны")
            await state.finish()    
        else:
            await message.answer("Введите пароль")
            await registration_teachers_status.Q1.set()
    except:
        await message.answer("Произошла ошибка 9102")
        await state.finish()

async def registration_teachers3(message: types.Message, state: FSMContext):
    try:
        a = BotDB.get_teachers_password(message.text)
        if(a == None):
            await message.answer("Неверный пароль")
            await state.finish()
        else:
            data = BotDB.get_teachers_data(a[0])
            data_2 = datetime.datetime.now()
            data_3 = datetime.datetime.strptime(data[0], '%Y-%m-%d %H:%M:%S.%f')
            data_4 = data_2 - data_3
            if int(data_4.days) == 0:
                await message.answer("Пароль верный\nДля регистрации введите ФИО")
                async with state.proxy() as data:
                    data['id'] = a[0]
                await registration_teachers_status.Q2.set()
            else:
                await message.answer("Неверный пароль")
                user_id = BotDB.get_teachers_user_id(a[0])
                BotDB.teachers_password_add(0, 0, user_id[0])
                await state.finish()
    except:
        await message.answer("Произошла ошибка 9103")
        await state.finish()


async def registration_teachers4(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            id = data['id']
        BotDB.teachers_add(message.text, message.from_user.id, id)
        await state.finish()
        await message.answer("Регистрация завершена")
        interface_all_begin(message, state)
    except:
        await message.answer("Произошла ошибка 9104")
        await state.finish()


def register_registration_teachers(dp: Dispatcher):
    all2 = all,None,test_status.Q1,test_status.Q2,rename_state.Q1,rename_state.Q2,reg_us.Q1
    dp.register_callback_query_handler(registration_teachers, lambda c: c.data == "registration_teachers", state=all.interface_all_stateBegin)
    dp.register_message_handler(registration_teachers2, commands=["registration"], state=all2)
    dp.register_message_handler(registration_teachers3, content_types = ['text'], state=registration_teachers_status.Q1)
    dp.register_message_handler(registration_teachers4, content_types = ['text'], state=registration_teachers_status.Q2)