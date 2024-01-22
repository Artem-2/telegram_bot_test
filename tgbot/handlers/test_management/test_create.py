import codecs
import os
from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, F
from tgbot.middlewares.DBhelp import BotDB
from tgbot.misc.states import all
from tgbot.handlers.interface_all import interface_all_begin
from tgbot.handlers.interface_all import interface_all_begin2
from aiogram.types import ContentType
from tgbot.misc.deleting_last_messages import deleting_last_messages


import random
import string
#ошибка 9300
#Доделать интерфейс

length = 10     #длинна кодового слова для теста

router = Router()

@router.callback_query(F.data == "test_create", all.interface_all_stateQ1)
async def test_create(call: types.CallbackQuery, state: FSMContext):
    try:
        keyboard =  InlineKeyboardBuilder()
        button_h = types.InlineKeyboardButton(text="Отмена", callback_data="start")
        keyboard.row(button_h)
        await call.message.answer("Отправьте файл формата .txt с тесто\nКодировка файла UTF-8",reply_markup = keyboard.as_markup())
        await state.set_state(state=all.test_readQ1)
    except:
        await call.message.answer("Произошла ошибка 9301")
        await state.clear()

@router.message(F.content_type == ContentType.DOCUMENT, all.test_readQ1)
async def test_create3(message: types.Message, state: FSMContext, bot:Bot):
    try:
        #получение содержимого файла
        if message.document.mime_type == 'text/plain':
            file_name = os.path.join(".", "Test_files", message.document.file_name)
            await bot.download(message.document.file_id, destination=file_name)
            with codecs.open(file_name, encoding='utf-8') as file:
                text = file.read()
            #генерация случайного кода
            result = 1
            while result != None:
                letters = string.ascii_uppercase
                rand_string = ''.join(random.choice(letters) for i in range(length))
                result = BotDB.get_test(rand_string)
        

            #обработка содержимого файла

            title = None
            time = 60
            mode = 0
            attempt = 1
            cost = 0
            mark_3 = 0
            mark_4 = 0
            mark_5 = 0

            flag = 0
            test_id = 0
            test_question_id = 0
            text = text.split(sep = '\n')
            for t in text:
                if flag == 0:
                    if t.startswith("\\title"):
                        t1 = t.replace("\\title ","")
                        t1 = t1.replace("\\title","")
                        title = t1

                    elif t.startswith("\\time_all"):
                        t1 = t.replace("\\time_all ","")
                        t1 = t1.replace("\\time_all","")
                        try:
                            time = int(t1)
                        except:
                            time = None
                            await message.answer("После \\time_all установлено не верное значение\nпо умолчанию 60")

                    elif t.startswith("\\random_mode"):
                        t1 = t.replace("\\random_mode ","")
                        t1 = t1.replace("\\random_mode","")
                        try:
                            mode = bool(int(t1))
                        except:
                            mode = 0
                            await message.answer("После \\random_mode установлено не верное значение\nпо умолчанию 0")
                    
                    elif t.startswith("\\number_of_attempts"):
                        t1 = t.replace("\\number_of_attempts ","")
                        t1 = t1.replace("\\number_of_attempts","")
                        try:
                            attempt = int(t1)
                        except:
                            attempt = 1
                            await message.answer("После \\number_of_attempts установлено не верное значение\nпо умолчанию 1")

                    elif t.startswith("\\number_of_questions"):
                        t1 = t.replace("\\number_of_questions ","")
                        t1 = t1.replace("\\number_of_questions","")
                        try:
                            cost = int(t1)
                        except:
                            cost = 0
                            await message.answer("После \\number_of_questions установлено не верное значение\nпо умолчанию 0")

                    elif t.startswith("\\3"):
                        t1 = t.replace("\\3 ","")
                        t1 = t1.replace("\\3","")
                        try:
                            mark_3 = int(t1)
                        except:
                            mark_3 = 0
                            await message.answer("После \\3 установлено не верное значение\nпо умолчанию 0")

                    elif t.startswith("\\4"):
                        t1 = t.replace("\\4 ","")
                        t1 = t1.replace("\\4","")
                        try:
                            mark_4 = int(t1)
                        except:
                            mark_4 = 0
                            await message.answer("После \\4 установлено не верное значение\nпо умолчанию 0")

                    elif t.startswith("\\5"):
                        t1 = t.replace("\\5 ","")
                        t1 = t1.replace("\\5","")
                        try:
                            mark_5 = int(t1)
                        except:
                            mark_5 = 0
                            await message.answer("После \\5 установлено не верное значение\nпо умолчанию 0")

                    elif t.startswith("\\q") and title == None and (mode == 0 or mode == 1) and cost == 0 and (0 <= mark_3 >= 5 and 0 <= mark_4 >= 5 and 0 <= mark_5 >= 5 ):
                        test_id = int(BotDB.test_add(message.from_user.id, title, rand_string, time, mode, attempt, cost, mark_3, mark_4, mark_5))
                        flag = 1

                if flag == 1:
                    if t.startswith("\\q"):
                        t1 = t.replace("\\q ","")
                        t1 = t1.replace("\\q","")
                        test_question_id = int(BotDB.question_test_add(test_id, t1.replace('\r', '')))

                    elif t.startswith("\\pictures"):
                        t1 = t.replace("\\pictures ","")
                        t1 = t1.replace("\\pictures","")
                        a = BotDB.get_pictures_id(t1[:-1])
                        if a !=None:
                            BotDB.question_test_add_pictures(t1[:-1],test_question_id)
                        else:
                            await message.answer("Код картинки: " + t1.replace('\r', '') + " не существует")

                    elif t.startswith("\\time"):
                        t1 = t.replace("\\time ","")
                        t1 = t1.replace("\\time","")
                        BotDB.answer_test_add_time(test_question_id, t1.replace('\r', ''))

                    elif t.startswith("\\-"):
                        t1 = t.replace("\\- ","")
                        t1 = t1.replace("\\-","")
                        BotDB.answer_test_add(test_question_id, t1.replace('\r', ''), 0)

                    elif t.startswith("\\+"):
                        t1 = t.replace("\\+ ","")
                        t1 = t1.replace("\\+","")
                        BotDB.answer_test_add(test_question_id, t1.replace('\r', ''), 1)

            if flag == 0:
                await message.answer("некоректный файл теста")
            else:
                await message.answer("Код теста : " + rand_string)
            await state.clear()
            file = os.path.join(".", "Test_files", message.document.file_name)
            os.remove(file)
            await interface_all_begin(message,state)
    except:
        await message.answer("Произошла ошибка 9302")
        await state.clear()


@router.callback_query(F.data == "test_create_help", all.interface_all_stateQ1)
async def test_create_help(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.answer("В разработке")
        await interface_all_begin2(call,state)
    except:
        await call.message.answer("Произошла ошибка 9303")
        await state.clear()
