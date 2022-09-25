import codecs
from mailbox import Message
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tgbot.middlewares.DBhelp import BotDB
from tgbot.misc.states import test_read
from tgbot.handlers.interface_all import interface_all_begin
from tgbot.handlers.interface_all import interface_all_begin2

import random
import string

#Доделать интерфейс

length = 10     #длинна кодового слова для теста

async def test_create(call: types.CallbackQuery):
    await call.message.answer("Отправьте файл формата .txt с тестом.\nДля отмены создания теста введите любое сообщение.")
    await test_read.Q1.set()


async def test_create2(message: types.Message, state: FSMContext):
    await message.answer("Создание теста отменено для того чтобы повторить попытку введите /test_create")
    await state.finish()


async def test_create3(message: types.Message, state: FSMContext):
    #получение содержимого файла
    if message.document.mime_type == 'text/plain':
        file_name = message.document.file_name
        await message.document.download(destination_file=file_name)
        with codecs.open(file_name, encoding='utf-8') as file:
            text = file.read()
        #генерация случайного кода
        result = 1
        while result != None:
            letters = string.ascii_uppercase
            rand_string = ''.join(random.choice(letters) for i in range(length))
            result = BotDB.get_test(rand_string)
        
        await message.answer("Код теста : " + rand_string)

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

                elif t.startswith("\\q"):
                    test_id = int(BotDB.test_add(message.from_user.id, title, rand_string, time, mode, attempt, cost, mark_3, mark_4, mark_5))
                    flag = 1

            if flag == 1:
                if t.startswith("\\q"):
                    t1 = t.replace("\\q ","")
                    t1 = t1.replace("\\q","")
                    test_question_id = int(BotDB.question_test_add(test_id, t1[:-1]))

                elif t.startswith("\\pictures"):
                    t1 = t.replace("\\pictures ","")
                    t1 = t1.replace("\\pictures","")
                    a = BotDB.get_pictures_id(t1[:-1])
                    if a !=None:
                        BotDB.question_test_add_pictures(t1[:-1],test_question_id)
                    else:
                        await message.answer("Код картинки: " + t1[:-1] + " не существует")

                elif t.startswith("\\time"):
                    t1 = t.replace("\\time ","")
                    t1 = t1.replace("\\time","")
                    BotDB.answer_test_add_time(test_question_id, t1[:-1])

                elif t.startswith("\\-"):
                    t1 = t.replace("\\- ","")
                    t1 = t1.replace("\\-","")
                    BotDB.answer_test_add(test_question_id, t1[:-1], 0)

                elif t.startswith("\\+"):
                    t1 = t.replace("\\+ ","")
                    t1 = t1.replace("\\+","")
                    BotDB.answer_test_add(test_question_id, t1[:-1], 1)

        await state.finish()
        await interface_all_begin(message,state)

async def test_create_help(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("для создания теста необходимо создать текстовый файл в формате .txt \nв начале файла укажите время которое будет дано для ответа на вопрос пример: \\t30(на каждый вопрос будет дано 30с)")
    await call.message.answer("перед каждым из вопросов \\q\n дальше варианты ответа на вопрос перед каждым из вариантов +(правльный вариант ответа) либо -(неправильный вариант ответа)\nпример:")
    await call.message.answer("\qздесь необходимо ввести вопрос\n-неправильный вариант ответа\n+правильный вариант ответа\n-неправильный вариант ответа\n-неправильный вариант ответа")
    await call.message.answer("все строчки у которых не будет указано \\t,\\q,-,+ считаются коментариями\nесли у вопроса несколько вариантов ответа отмечены + то каждый из ответов будет считаться правильным")
    await interface_all_begin2(call,state)

def register_test_create(dp: Dispatcher):
    dp.register_callback_query_handler(test_create, lambda c: c.data == "test_create", state=None)
    dp.register_callback_query_handler(test_create_help,  lambda c: c.data == "test_create_help", state=None)
    dp.register_message_handler(test_create3,content_types = ['document'], state=test_read.Q1)
    dp.register_message_handler(test_create2,content_types = ['text'], state=test_read.Q1)