import os.path
import datetime
import asyncio
import copy
from aiogram.utils.exceptions import MessageNotModified
from contextlib import suppress
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import (MessageCantBeDeleted, MessageToDeleteNotFound, )
from aiogram.types import InlineKeyboardMarkup
from tgbot.middlewares.DBhelp import BotDB
from tgbot.misc.states import test_status_v2,all
from tgbot.handlers.interface_all import interface_all_begin, interface_all_begin4
import random
#ошибки 6000
time_update = 5 #частота обновления таймера

#проверка git

#класс для переменной теста
class question_class(object):
    def __init__(self):
        #номер вопроса
        self.question_number = None
        #id сообщения если есть
        self.message_id = None
        #тип вопроса
        self.type = None    #"text","one_answer","many_answers"
        #id вопроса
        self.question_id = None
        #текст вопроса
        self.text_question = None
        #переменная с кнопками
        self.button = None
        #код фото
        self.photo = None
        #все варианты ответа (текст ответа, правильный ли ответ, id ответа)
        self.answers = None
        #время ответа(оставшееся время)
        self.response_time = None
        #выбранный(е) вариант ответа
        self.selected_answer_option = None
        #текстовый ответ на вопрос
        self.text_response = None
        #номер правильного ответа
        self.correct_answer_number = None
        #есть ли вопрос в базе данных
        self.response_id_in_the_database = None

    #создание основных кнопок
    def button_create(self):
        if self.answers != None:
            i = 0
            self.button =  InlineKeyboardMarkup()
            for answer in random.sample(self.answers,len(self.answers)):
                self.text_question = self.text_question + "\n" + chr(ord('a') + i) + ") " + str(answer[0])

                if self.selected_answer_option != None:
                    #проверка не выбран ли вариант ответа
                    if i in self.selected_answer_option:
                        button_h = types.InlineKeyboardButton("[" + str(ord('a') + i) + "]", callback_data = str(i))
                    else:
                        button_h = types.InlineKeyboardButton(chr(ord('a') + i), callback_data = str(i))
                else:
                    button_h = types.InlineKeyboardButton(chr(ord('a') + i), callback_data = str(i))
                if self.type == "one_answer":
                    if answer[1] == 1:
                        self.correct_answer_number = i
                else:
                    if answer[1] == 1:
                        if type(self.correct_answer_number) == list:
                            self.correct_answer_number.append(i)
                        else:
                            self.correct_answer_number = [i]
                i = i+1
                self.button.add(button_h)
    
    #создание кнопок времмени и перехода на следующий или приведущий вопрос
    def button_create_time_and_auxiliary_buttons(self, len_test):
        button = copy.deepcopy(self.button)
        if self.question_number == 0:
            button_h_2 = types.InlineKeyboardButton("Далее", callback_data = "next")
            button.add(button_h_2)
        elif self.question_number != 0 and self.question_number != len_test-1:
            button_h_1 = types.InlineKeyboardButton("Назад", callback_data = "prev")
            button_h_2 = types.InlineKeyboardButton("Далее", callback_data = "next")
            button.row(button_h_1, button_h_2)
        else:
            button_h_1 = types.InlineKeyboardButton("Назад", callback_data = "prev")
            button_h_2 = types.InlineKeyboardButton("Закончить тест", callback_data = "finish_the_test")
            button.row(button_h_1, button_h_2)
        button_h_1 = types.InlineKeyboardButton("Осталось времени: " + str(int(self.response_time)) + "c", callback_data = "None")
        button_h_2 = types.InlineKeyboardButton(str(self.question_number + 1) + "-й вопрос из " + str(len_test), callback_data = "None")
        button.row(button_h_1, button_h_2)
        return button 
    
    #удаление сообщений через определенное время
    async def deleting_messages_after_time_has_elapsed(self):
        await asyncio.sleep(self.response_time)
        try:
            await self.message_id.delete()
            self.message_id = None
            self.response_time = 0
        except:
            pass
    
    #удаление сообщений 
    async def deleting_messages(self):
        try:
            await self.message_id.delete()
            self.message_id = None
        except:
            pass

    #обновление времени в сообщения
    async def updating_the_time_in_the_message(self, len_test):
        r_time = self.response_time
        time = datetime.datetime.now()
        while self.message_id != None:
            await asyncio.sleep(time_update)
            time2 = datetime.datetime.now() - time
            self.response_time = r_time - int(time2.seconds)
            try:
                button = self.button_create_time_and_auxiliary_buttons(len_test)
                #изменение кнопок
                await self.message_id.edit_reply_markup(reply_markup = button)
            except:
                pass




###################################################################################################################################
#начальная функция запрашивает код теста
async def code_request(call: types.CallbackQuery, state: FSMContext):
    button =  InlineKeyboardMarkup()
    button_h = types.InlineKeyboardButton(("Отмена"), callback_data = "start")
    button.add(button_h)
    await call.message.answer("Введите код теста", reply_markup = button)
    await test_status_v2.Q1.set()
    
###################################################################################################################################
#в данной функции выводится основная информация о тесте и выдает запрос на начало теста
async def output_information_about_test(message: types.Message, state: FSMContext):
    #проверка существования теста
    code = BotDB.get_test(message.text)
    if code != None:
        test_id = code[0]
        #запрос всех необходимых данных из базы данных
        user_id = BotDB.user_exists(message.from_user.id)
        questions = BotDB.get_question_test(test_id)
        title, number_of_attempts, random_mode, len_test = BotDB.get_test_title_attempts_random_mode_questions(test_id)
        t = BotDB.get_test_result(user_id[0], test_id)
        #вывод информации о тесте
        await message.answer("Название теста: "+str(title[:-1]))
        await message.answer("Количество попыток: "+str(number_of_attempts))
        await message.answer("Количество использованных попыток: "+str(len(t)))
        if random_mode:   #при не случайном выборе вопросов не указывается количество вопросов
            await message.answer("Количество вопросов: "+str(len_test))
        else:
            await message.answer("Количество вопросов: "+str(len(questions)))
        #проверка на активировнн ли тест
        active_mode = BotDB.get_test_active_mode(test_id)
        if active_mode[0]:
            if int(len(t)) < int(number_of_attempts):
                #передача данных в машину состояний
                async with state.proxy() as data:
                    data["time_question"] = code[1]
                    data["test_id"] = code[0]
                    data["user_id"] = user_id[0]
                    data["questions"] = questions
                    data["random_mode"] = random_mode
                    data["len_test"] = len_test
                #создание клавиатуры для начала тестирования
                button =  InlineKeyboardMarkup()
                button_h = types.InlineKeyboardButton(text="Начать тестирование", callback_data="start_test")
                button.add(button_h)
                button_h = types.InlineKeyboardButton(text="Назад", callback_data="start")
                button.add(button_h)
                await message.answer("Выберите вариант",reply_markup = button)
                #изменение состояния
                await test_status_v2.Q2.set()
            else:
                await message.answer("Вы уже проходили данный тест")
                await state.finish()
                await interface_all_begin(message, state)
        else:
            await message.answer("Тест не активен")
            await state.finish()
            await interface_all_begin(message, state)
    else:
        await message.answer("Данного теста не существует")
        await state.finish()
        await interface_all_begin(message, state)

###################################################################################################################################
#создает переменную с тестом
async def creates_variable_with_a_test(call: types.CallbackQuery, state: FSMContext):
    #получение всех необходимых данных из машины состояний
    async with state.proxy() as data:
        questions = data["questions"]
        random_mode = data["random_mode"]
        len_test = data["len_test"]
        time_question = data["time_question"]
        test_id = data["test_id"]
        user_id = data["user_id"]
    #добавление в базу данных начало прохождения теста
    id_of_the_test_results = BotDB.test_result_add(user_id,test_id)
    print(id_of_the_test_results)
    #определение вопросов которые будут в тесте
    selected_questions = []
    if random_mode == 1:
        for question in random.sample(questions,len_test):
            selected_questions.append(question)
    else:
        selected_questions = questions
    #определение переменной с вопросами
    all_question_data = []
    i = 0
    for question in selected_questions:
        #вспомогательная переменная
        question_data = question_class()
        #определение номера вопроса
        question_data.question_number = i
        #определение типа вопроса
        correct_answers = BotDB.get_answer_test_right_v2(question[0])
        #составление заголовка вопроса
        text = "Вопрос:\n" + str(question[1])
        if len(correct_answers) > 1:
            text = text + "\n\nВопрос с несколькими вариантами ответа"
            question_data.type = "text"
        elif len(correct_answers) == 1:
            text = text + "\n\nВопрос с одним вариантом ответа"
            question_data.type = "one_answer"
        elif len(correct_answers) == 1:
            text = text + "\n\nВопрос с текстовым ответом"
            question_data.type = "many_answers"
        #добавление в переменную всех вариантов ответа на данный вопрос
        answers = BotDB.get_answer_test(question[0])
        question_data.answers = answers
        #добавление в переменную id вопроса
        question_data.question_id = question[0]
        #добавление в переменную текста вопроса
        question_data.text_question = text
        #добавление в переменную кода картинки если есть
        photo_code = BotDB.get_question_test_pictures_id(question[0])
        photo = None
        if(photo_code[0] != None):
            photo = os.path.join(".","pictures",str(photo_code[0])+".png")
        question_data.photo = photo
        #добавление в переменную времени ответа
        if question[2] == 0:
            question_data.response_time = time_question
        else:
            question_data.response_time = question[2]
        #создание основных кнопок
        question_data.button_create()
        all_question_data.append(question_data)
        i += 1
    async with state.proxy() as data:
        data["all_question_data"] = all_question_data
        data["id_of_the_test_results"] = id_of_the_test_results
        data["question_number"] = 0
    await sending_a_message(call.message, state)

###################################################################################################################################
#прохождение теста отправка одного вопроса
async def sending_a_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        all_question_data = data["all_question_data"]
        question_number = data["question_number"]
        len_test = data["len_test"]
    #выбор необходимого вопроса
    question_data = all_question_data[question_number]
    #создание кнопопк
    button = question_data.button_create_time_and_auxiliary_buttons(len_test)
    #отправка сообщения
    if question_data.photo != None:
        all_question_data[question_number].message_id = await message.answer_photo(question_data.photo, caption = question_data.text_question, reply_markup = button)
    else:
        all_question_data[question_number].message_id = await message.answer(text = question_data.text_question, reply_markup = button)
    #запуск удаления сообщения
    asyncio.create_task(all_question_data[question_number].deleting_messages_after_time_has_elapsed())
    #запуск обновления таймера сообщения
    asyncio.create_task(all_question_data[question_number].updating_the_time_in_the_message(len_test))
    if all_question_data[question_number].type == "text":
        await test_status_v2.Q4.set()
    else:
        await test_status_v2.Q3.set()
    async with state.proxy() as data:
        data["all_question_data"] = all_question_data

###################################################################################################################################
async def callbacks_next_prev(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        id_of_the_test_results = data["id_of_the_test_results"]
        all_question_data = data["all_question_data"]
        question_number = data["question_number"]
        len_test = data["len_test"]
    question_data = all_question_data[question_number]
    #проверка есть ли вопрос в базе данных и есть ли ответ на него
    if question_data.response_id_in_the_database != None and question_data.selected_answer_option != None:
        #проверка на тип вопроса
        if question_data.type == "one_answer":
            is_correct_answer = question_data.correct_answer_number == question_data.selected_answer_option
            #отправка результата в базу данных
            BotDB.answer_question_result_update(question_data.response_id_in_the_database, id_of_the_test_results, is_correct_answer,question_data.question_id,question_data.answers[question_data.selected_answer_option])
        elif question_data.type == "many_answers":
            helper_1 = question_data.correct_answer_number.sort()
            helper_2 = question_data.selected_answer_option.sort()
            is_correct_answer = helper_1 == helper_2
            answers = []
            for s in question_data.selected_answer_option:
                answers.append(question_data.answers[s])
            #отправка результата в базу данных
            BotDB.answer_question_result_update(question_data.response_id_in_the_database, id_of_the_test_results, is_correct_answer,question_data.question_id,answers)
    #удаление текущего сообщения
    question_data.deleting_messages()
    #переход на следующий или приведущий вопрос
    all_question_data[question_number] = question_data
    if call.data == "next":
        #проверка есть ли вопрос до в котором не вышло время
        for i in reversed(list(range(question_number + 1,len_test))):
            if all_question_data[i] != 0:
                question_number = i
    else:
        #проверка есть ли вопрос после в котором не вышло время
        for i in list(range(0,question_number)):
            if all_question_data[i] != 0:
                question_number = i
    async with state.proxy() as data:
        data["question_number"] = question_number
        data["all_question_data"] = all_question_data
    await sending_a_message(call.message, state)
    
    
###################################################################################################################################
async def text_response(message: types.Message, state: FSMContext):
    pass


def register_passing_the_test_v2(dp: Dispatcher):
    dp.register_callback_query_handler(code_request, lambda c: c.data == "passing_the_test_v2", state=all.interface_all_stateQ1)
    dp.register_message_handler(output_information_about_test, content_types = ['text'], state=test_status_v2.Q1)
    dp.register_callback_query_handler(creates_variable_with_a_test,lambda c: c.data == "start_test", state=test_status_v2.Q2)
    #dp.register_message_handler(text_response,content_types = ['text'], state=test_status_v2.Q3)
    dp.register_callback_query_handler(callbacks_next_prev, lambda c: c.data == "next" or c.data == "prev", state=test_status_v2.Q3)
    #dp.register_callback_query_handler(callbacks_finish_the_test, lambda c: c.data == "prev", state=test_status_v2.Q3)
    #dp.register_callback_query_handler(callbacks, state=test_status_v2.Q3)