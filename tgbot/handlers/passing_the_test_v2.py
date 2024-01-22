import os.path
import datetime
import asyncio
import copy
from aiogram.types import FSInputFile
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, F
from tgbot.middlewares.DBhelp import BotDB
from tgbot.misc.states import test_status_v2,all
from tgbot.handlers.interface_all import interface_all_begin, interface_all_begin2
import random
#ошибки 6000
from tgbot.misc.config import config
time_update = config.tg_bot.time_update #частота обновления таймера




router = Router()
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
        self.keyboard = None
        #код фото
        self.photo = None
        #все варианты ответа (текст ответа, правильный ли ответ, id ответа)
        self.answers = None
        self.random_answers = None
        #время ответа(оставшееся время)
        self.response_time = None
        #выбранный(е) вариант ответа
        self.selected_answer_option = []
        #текстовый ответ на вопрос (текст ответа, id ответа)
        self.text_response = None
        #номер правильного ответа
        self.correct_answer_number = []
        #есть ли вопрос в базе данных
        self.response_id_in_the_database = []

    #создание основных кнопок
    def button_create(self):
        flag = False
        if self.correct_answer_number == []:
            flag = True
        if self.answers != None:
            i = 0
            self.keyboard =  InlineKeyboardBuilder()
            for answer in self.random_answers:
                self.text_question = self.text_question + "\n" + chr(ord('a') + i) + ") " + str(answer[0])

                if self.selected_answer_option != None:
                    #проверка не выбран ли вариант ответа
                    if i in self.selected_answer_option:
                        button_h = types.InlineKeyboardButton(text = "[" + chr(ord('a') + i) + "]", callback_data = str(i))
                    else:
                        button_h = types.InlineKeyboardButton(text = chr(ord('a') + i), callback_data = str(i))
                else:
                    button_h = types.InlineKeyboardButton(text = chr(ord('a') + i), callback_data = str(i))
                if flag == True:
                    if self.type == "one_answer":
                        if answer[1] == 1:
                            self.correct_answer_number = i
                    else:
                        if answer[1] == 1:
                            self.correct_answer_number.append(i)
                i = i+1
                self.keyboard.row(button_h)
    
    #создание кнопок времмени и перехода на следующий или приведущий вопрос
    def button_create_time_and_auxiliary_buttons(self, len_test):
        keyboard = copy.deepcopy(self.keyboard)
        if self.question_number == 0:
            button_h_2 = types.InlineKeyboardButton(text = "Далее", callback_data = "next")
            keyboard.row(button_h_2)
        elif self.question_number != 0 and self.question_number != len_test-1:
            button_h_1 = types.InlineKeyboardButton(text = "Назад", callback_data = "prev")
            button_h_2 = types.InlineKeyboardButton(text = "Далее", callback_data = "next")
            keyboard.row(button_h_1, button_h_2)
        else:
            button_h_1 = types.InlineKeyboardButton(text = "Назад", callback_data = "prev")
            button_h_2 = types.InlineKeyboardButton(text = "Закончить тест", callback_data = "finish_the_test")
            keyboard.row(button_h_1, button_h_2)
        button_h_1 = types.InlineKeyboardButton(text = "Осталось времени: " + str(int(self.response_time)) + "c", callback_data = "None")
        button_h_2 = types.InlineKeyboardButton(text = str(self.question_number + 1) + "-й вопрос из " + str(len_test), callback_data = "None")
        keyboard.row(button_h_1, button_h_2)
        return keyboard 
    
    #удаление сообщений через определенное время
    async def deleting_messages_after_time_has_elapsed(self, len_test, state: FSMContext, message: types.Message):
        await asyncio.sleep(self.response_time)
        try:
            await self.message_id.delete()
            data = await state.get_data()
            all_question_data = data["all_question_data"]
            all_question_data[self.question_number].response_time = 0
            #проверка есть ли вопрос после в котором не вышло время
            halper = self.question_number
            for i in reversed(list(range(self.question_number + 1,len_test))):
                if all_question_data[i].response_time != 0:
                    self.question_number = i
            #проверка есть ли вопрос до в котором не вышло время при условии что нет вопроса после
            if halper == self.question_number:
                for i in list(range(0,self.question_number)):
                    if all_question_data[i].response_time != 0:
                        self.question_number = i
            #костыль переходник
            class call:
                message: int
                from_user: int
            call.message = message
            call.from_user = message.chat
            #если вопросов не осталось завершить тест
            if halper == self.question_number:
                await callbacks_finish_the_test(call, state)
            await state.update_data(question_number=self.question_number)
            await state.update_data(all_question_data=all_question_data)
            await sending_a_message(message, state)
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
    async def updating_the_time_in_the_message(self, len_test, state: FSMContext):
        try:
            data = await state.get_data()
            question_number = data["question_number"]

            r_time = self.response_time
            time = datetime.datetime.now()
            flag_exit = 1
            helper = 0
            while flag_exit != 0:
                await asyncio.sleep(1)
                data = await state.get_data()
                question_number_helper = data["question_number"]
                all_question_data = data["all_question_data"]
                time2 = datetime.datetime.now() - time
                all_question_data[question_number].response_time = r_time - int(time2.total_seconds())
                if int(time2.total_seconds()) // 5 > helper:
                    helper = int(time2.total_seconds()) // 5
                    try:
                        if question_number_helper == question_number:
                            keyboard = all_question_data[question_number].button_create_time_and_auxiliary_buttons(len_test)
                            await state.update_data(all_question_data=all_question_data)
                            #изменение кнопок
                            await all_question_data[question_number].message_id.edit_reply_markup(reply_markup = keyboard.as_markup())
                        else:
                            flag_exit = 0
                            await state.update_data(all_question_data=all_question_data)
                    except:
                        flag_exit = 0
                        await state.update_data(all_question_data=all_question_data)
                else:
                    if question_number_helper != question_number:
                        flag_exit = 0
                        await state.update_data(all_question_data=all_question_data)
        except:
            pass


###################################################################################################################################
#начальная функция запрашивает код теста
@router.callback_query(F.data == "passing_the_test_v2", all.interface_all_stateQ1)
async def code_request(call: types.CallbackQuery, state: FSMContext):
    keyboard =  InlineKeyboardBuilder()
    button_h = types.InlineKeyboardButton(text="Отмена", callback_data = "start")
    keyboard.row(button_h)
    await call.message.answer("Введите код теста", reply_markup = keyboard.as_markup())
    await state.set_state(state=test_status_v2.Q1)
    
###################################################################################################################################
#в данной функции выводится основная информация о тесте и выдает запрос на начало теста
@router.message(F.text, test_status_v2.Q1)
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
                await state.update_data(time_question=code[1])
                await state.update_data(test_id=code[0])
                await state.update_data(user_id=user_id[0])
                await state.update_data(questions=questions)
                await state.update_data(random_mode=random_mode)
                await state.update_data(len_test=len_test)
                #создание клавиатуры для начала тестирования
                keyboard =  InlineKeyboardBuilder()
                button_h = types.InlineKeyboardButton(text="Начать тестирование", callback_data="start_test")
                keyboard.row(button_h)
                button_h = types.InlineKeyboardButton(text="Назад", callback_data="start")
                keyboard.row(button_h)
                await message.answer("Выберите вариант",reply_markup = keyboard.as_markup())
                #изменение состояния
                await state.set_state(state=test_status_v2.Q2)
            else:
                await message.answer("Вы уже проходили данный тест")
                await state.clear()
                await interface_all_begin(message, state)
        else:
            await message.answer("Тест не активен")
            await state.clear()
            await interface_all_begin(message, state)
    else:
        await message.answer("Данного теста не существует")
        await state.clear()
        await interface_all_begin(message, state)

###################################################################################################################################
#создает переменную с тестом
@router.callback_query(F.data == "start_test", test_status_v2.Q2)
async def creates_variable_with_a_test(call: types.CallbackQuery, state: FSMContext):
    #получение всех необходимых данных из машины состояний
    data = await state.get_data()
    questions = data["questions"]
    random_mode = data["random_mode"]
    len_test = data["len_test"]
    time_question = data["time_question"]
    test_id = data["test_id"]
    user_id = data["user_id"]
    #добавление в базу данных начало прохождения теста
    id_of_the_test_results = BotDB.test_result_add(user_id,test_id)
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
            question_data.type = "many_answers"
            question_data.response_id_in_the_database = BotDB.answer_question_result_multiple_answers(id_of_the_test_results,False,question[0],"multiple_answers:,")
        elif len(correct_answers) == 1:
            text = text + "\n\nВопрос с одним вариантом ответа"
            question_data.type = "one_answer"
            question_data.response_id_in_the_database = BotDB.answer_question_result(id_of_the_test_results,False,question[0],0)
        elif len(correct_answers) == 0:
            text = text + "\n\nВопрос с текстовым ответом"
            question_data.type = "text"
            question_data.response_id_in_the_database = BotDB.answer_question_result_multiple_answers(id_of_the_test_results,False,question[0],"multiple_answers:,")
        #добавление в переменную всех вариантов ответа на данный вопрос
        answers = BotDB.get_answer_test(question[0])
        question_data.answers = answers
        question_data.random_answers = random.sample(answers,len(answers))
        #добавление в переменную id вопроса
        question_data.question_id = question[0]
        #добавление в переменную текста вопроса
        question_data.text_question = text
        #добавление в переменную кода картинки если есть
        photo_code = BotDB.get_question_test_pictures_id(question[0])
        photo = None
        if(photo_code[0] != None):
            photo = os.path.join(".","pictures",str(photo_code[0])+".png")
            photo = FSInputFile(photo)
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
    await state.update_data(all_question_data=all_question_data)
    await state.update_data(id_of_the_test_results=id_of_the_test_results)
    await state.update_data(question_number=0)
    await sending_a_message(call.message, state)

###################################################################################################################################
#прохождение теста отправка одного вопроса
async def sending_a_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    all_question_data = data["all_question_data"]
    question_number = data["question_number"]
    len_test = data["len_test"]
    #выбор необходимого вопроса
    question_data = all_question_data[question_number]
    #создание кнопопк
    keyboard = question_data.button_create_time_and_auxiliary_buttons(len_test)
    #отправка сообщения
    if question_data.photo != None:
        all_question_data[question_number].message_id = await message.answer_photo(question_data.photo, caption = question_data.text_question, reply_markup = keyboard.as_markup())
    else:
        all_question_data[question_number].message_id = await message.answer(text = question_data.text_question, reply_markup = keyboard.as_markup())
    #запуск удаления сообщения
    asyncio.create_task(all_question_data[question_number].deleting_messages_after_time_has_elapsed(len_test,state,message))
    #запуск обновления таймера сообщения
    asyncio.create_task(all_question_data[question_number].updating_the_time_in_the_message(len_test, state))
    if all_question_data[question_number].type == "text":
        await state.set_state(state=test_status_v2.Q4)
    else:
        await state.set_state(state=test_status_v2.Q3)
    await state.update_data(all_question_data=all_question_data)

###################################################################################################################################
@router.callback_query(F.data == "next", test_status_v2.Q4)
@router.callback_query(F.data == "prev", test_status_v2.Q4)
@router.callback_query(F.data == "next", test_status_v2.Q3)
@router.callback_query(F.data == "prev", test_status_v2.Q3)
@router.callback_query(F.data == "finish_the_test", test_status_v2.Q3)
async def callbacks_next_prev(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    id_of_the_test_results = data["id_of_the_test_results"]
    all_question_data = data["all_question_data"]
    question_number = data["question_number"]
    len_test = data["len_test"]
    question_data = all_question_data[question_number]
    #проверка есть ли вопрос в базе данных и есть ли ответ на него
    if question_data.response_id_in_the_database != None and question_data.selected_answer_option != None:
        #проверка на тип вопроса
        if question_data.type == "one_answer" and question_data.selected_answer_option != []:
            is_correct_answer = question_data.correct_answer_number == question_data.selected_answer_option[0]
            #отправка результата в базу данных
            BotDB.answer_question_result_update(question_data.response_id_in_the_database, id_of_the_test_results, is_correct_answer,question_data.question_id,question_data.answers[question_data.selected_answer_option[0]][2])
        elif question_data.type == "many_answers" and question_data.selected_answer_option != []:
            helper_1 = sorted(question_data.correct_answer_number)
            helper_2 = sorted(question_data.selected_answer_option)
            is_correct_answer = helper_1 == helper_2
            answers = []
            for s in question_data.selected_answer_option:
                answers.append(question_data.answers[s][2])
            #отправка результата в базу данных
            BotDB.answer_question_result_multiple_answers_update(question_data.response_id_in_the_database, id_of_the_test_results, is_correct_answer,question_data.question_id,"multiple_answers:," + ",".join(str(x) for x in answers))
    #удаление текущего сообщения
    await question_data.deleting_messages()
    #переход на следующий или приведущий вопрос
    all_question_data[question_number] = question_data
    if call.data == "next":
        #проверка есть ли вопрос после в котором не вышло время
        for i in reversed(list(range(question_number + 1,len_test))):
            if all_question_data[i].response_time != 0:
                question_number = i
    elif call.data == "prev":
        #проверка есть ли вопрос до в котором не вышло время
        for i in list(range(0,question_number)):
            if all_question_data[i].response_time != 0:
                question_number = i
    await state.update_data(question_number=question_number)
    await state.update_data(all_question_data=all_question_data)
    if call.data == "finish_the_test":
        await callbacks_finish_the_test(call, state)
    else:
        await sending_a_message(call.message, state)
    
    
###################################################################################################################################
@router.message(F.text, test_status_v2.Q4)
async def text_response(message: types.Message, state: FSMContext):
    data = await state.get_data()
    all_question_data = data["all_question_data"]
    question_number = data["question_number"]
    len_test = data["len_test"]
    question_data = all_question_data[question_number]
    #занесение в бд
    BotDB.answer_question_result_text_response_update(question_data.response_id_in_the_database, message.text)
    await question_data.deleting_messages()
    #переход на следующий вопрос
    for i in reversed(list(range(question_number + 1,len_test))):
        if all_question_data[i].response_time != 0:
            question_number_next = i

    all_question_data[question_number].text_response = message.text
    await state.update_data(question_number=question_number_next)
    await state.update_data(all_question_data=all_question_data)
    await sending_a_message(message, state)

###################################################################################################################################
async def callbacks_finish_the_test(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    all_question_data = data["all_question_data"]
    id_of_the_test_results = data["id_of_the_test_results"]
    test_id = data["test_id"]
    results = BotDB.get_question_result(id_of_the_test_results)
    mark = BotDB.get_test_mark(test_id)
    sum = 0
    cost = 0
    mark1 = 0
    number_of_text_questions = 0
    for a in all_question_data:
        if a.type == "text":
            number_of_text_questions = number_of_text_questions + 1
    if mark[1] == 0 and mark[0] == 0 and mark[2] == 0:
        await call.message.answer("Тест пройден")
        BotDB.test_result_add_result("Тест пройден", id_of_the_test_results, "None")
    elif mark[1] == 0 and mark[0] == 0 and mark[2] != 0:
        for r in results:
            if r[0] != None:
                sum = sum + r[0]
                cost = cost + 1
        await call.message.answer(str(sum)+" правильных ответов из "+str(cost - number_of_text_questions))
        if int(mark[2]) <= sum:
            await call.message.answer("Тест сдан")
            BotDB.test_result_add_result(str(sum)+"/"+str(cost - number_of_text_questions), id_of_the_test_results, "Тест сдан")
        else:
            await call.message.answer("Тест не сдан")
            BotDB.test_result_add_result(str(sum)+"/"+str(cost - number_of_text_questions), id_of_the_test_results, "Тест не сдан")
    else:
        for r in results:
            if r[0] != None:
                sum = sum + r[0]
                cost = cost + 1
        if int(mark[2]) <= sum:
            mark1 = 5
        elif int(mark[1]) <= sum:
            mark1 = 4
        elif int(mark[0]) <= sum:
            mark1 = 3
        else:
            mark1 = 2
        await call.message.answer(str(sum)+" правильных ответов из "+str(cost - number_of_text_questions))
        await call.message.answer("Оценка: "+str(mark1))
        BotDB.test_result_add_result(str(sum)+"/"+str(cost), id_of_the_test_results, mark1)
    await state.clear()
    await interface_all_begin2(call, state)


###################################################################################################################################
@router.callback_query(test_status_v2.Q3)
async def callbacks(call: types.CallbackQuery, state: FSMContext):
    flag = 0
    flag_answers = False
    try:
        call_data = int(call.data)
    except:
        flag = 1
    if flag == 0:
        data = await state.get_data()
        all_question_data = data["all_question_data"]
        question_number = data["question_number"]
        len_test = data["len_test"]
        question_data = all_question_data[question_number]
        if question_data.type == "one_answer":
            if question_data.selected_answer_option != [call_data]:
                question_data.selected_answer_option = [call_data]
                flag_answers = True
        else:
            if not(call_data in question_data.selected_answer_option):
                question_data.selected_answer_option.append(call_data)
                question_data.selected_answer_option.sort()
                flag_answers = True
            else:
                question_data.selected_answer_option.remove(call_data)
                question_data.selected_answer_option.sort()
                flag_answers = True

        if flag_answers:
            question_data.button_create()
            keyboard = question_data.button_create_time_and_auxiliary_buttons(len_test)
            await question_data.message_id.edit_reply_markup(reply_markup = keyboard.as_markup())
            all_question_data[question_number].keyboard = question_data.keyboard
            all_question_data[question_number].selected_answer_option = question_data.selected_answer_option
            await state.update_data(all_question_data=all_question_data)
