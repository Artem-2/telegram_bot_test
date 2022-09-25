import os.path
import asyncio
from contextlib import suppress
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import (MessageCantBeDeleted, MessageToDeleteNotFound, )
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.middlewares.DBhelp import BotDB
from tgbot.misc.states import test_status
from tgbot.handlers.interface_all import interface_all_begin
import random





###################################################################################################################################
async def update_message(call: types.CallbackQuery, state: FSMContext, call_data):
    try:
        async with state.proxy() as data:
            msg = data['msg']
            i = data['i']
        button =  InlineKeyboardMarkup()
        for j in range(msg[i-1][6]):
            if int(call_data) != j :
                button_h = types.InlineKeyboardButton(chr(ord('a') + j), callback_data = str(j))
                button.add(button_h)
            else:
                button_h = types.InlineKeyboardButton("[" + chr(ord('a') + j) + "]", callback_data = str(j))
                #button_h = types.InlineKeyboardButton("Выбран - " + chr(ord('a') + j), callback_data = str(j))
                button.add(button_h)
        button_h = types.InlineKeyboardButton("Далее", callback_data = "next")
        button.add(button_h)
        await call.message.edit_reply_markup(reply_markup=button)
    except:
        pass
###################################################################################################################################
async def update_message_multiple_answers(call: types.CallbackQuery, state: FSMContext, call_data_multiple_answers):
    try:
        async with state.proxy() as data:
            msg = data['msg']
            i = data['i']
        j1 = 0
        button =  InlineKeyboardMarkup()
        for j in range(msg[i-1][6]):
            if len(call_data_multiple_answers) > j1:
                if call_data_multiple_answers[j1] != str(j) :
                    button_h = types.InlineKeyboardButton(chr(ord('a') + j), callback_data = str(j))
                    button.add(button_h)
                else:
                    button_h = types.InlineKeyboardButton("[" + chr(ord('a') + j) + "]", callback_data = str(j))
                    #button_h = types.InlineKeyboardButton("Выбран - " + chr(ord('a') + j), callback_data = str(j))
                    button.add(button_h)
                    j1 = j1 + 1
            else:
                button_h = types.InlineKeyboardButton(chr(ord('a') + j), callback_data = str(j))
                button.add(button_h)
        button_h = types.InlineKeyboardButton("Далее", callback_data = "next")
        button.add(button_h)
        await call.message.edit_reply_markup(reply_markup=button)
    except:
        pass
###################################################################################################################################
#удаление сообщений через определенное время
async def delete_message(state: FSMContext, message: types.Message, sleep_time: int = 0, mode: int = 0):
    try:
        async with state.proxy() as data:
            msg = data['msg']
            i = data['i']
        await asyncio.sleep(sleep_time)
        with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        
            if sleep_time != 0: 
                await message.delete()
                async with state.proxy() as data:
                    user = data['user']
                    test = data['test']
                    call_data = data['call_data']
                id1 = BotDB.get_test_result(user, test)
                if mode == 0:
                    if call_data == -1:
                        BotDB.answer_question_result2(id1[len(id1)-1][0],False,msg[i-1][4])
                    else:
                        async with state.proxy() as data:
                            user = data['user']
                            test = data['test']
                            msg = data['msg']
                            i = data['i']
                        id2 = BotDB.get_test_result(user,test)
                        id1 = id2[len(id2)-1][0]
                        #проверка правильности ответа
                        if str(msg[i-1][2][0]) == call_data:
                            
                            await message.answer(str(call_data))
                            BotDB.answer_question_result(id1,True,msg[i-1][4],msg[i-1][5][int(call_data)])
                        else: 
                            await message.answer(str(call_data))
                            BotDB.answer_question_result(id1,False,msg[i-1][4],msg[i-1][5][int(call_data)])
                        async with state.proxy() as data:
                            data['call_data'] = -1
                else:
                    BotDB.answer_question_result_text_response(id1[len(id1)-1][0],msg[i-1][1],"None")
                await passing_the_test3(message, state)
            else:
                await message.delete()
    except:
        pass
###################################################################################################################################
#вспомогательная
async def passing_the_test(call: types.CallbackQuery):
    await call.message.answer("Введите код теста")
    await test_status.Q1.set()


async def passing_the_test1(message: types.Message, state: FSMContext):
    code = BotDB.get_test(message.text)
    if code != None:
        test_id = code[0]
        user_id = BotDB.user_exists(message.from_user.id)
        question = BotDB.get_question_test(test_id)
        title = BotDB.get_test_title(test_id)
        a = BotDB.get_test_attempts(test_id)
        t = BotDB.get_test_result(user_id[0], test_id)
        len_test = BotDB.get_test_questions(test_id)
        i1 = BotDB.get_test_random_mode(test_id)
        if i1[0]:
            await message.answer("Название теста: "+str(title[0][:-1]))
            await message.answer("Количество попыток: "+str(a[0]))
            await message.answer("Количество использованных попыток: "+str(len(t)))
            await message.answer("Количество вопросов: "+str(len_test[0]))
        else:
            await message.answer("Название теста: "+str(title[0][:-1]))
            await message.answer("Количество попыток: "+str(a[0]))
            await message.answer("Количество использованных попыток: "+str(len(t)))
            await message.answer("Количество вопросов: "+str(len(question)))
        active_mode = BotDB.get_test_active_mode(test_id)
        if active_mode[0]:
            if int(len(t)) < int(a[0]):
                async with state.proxy() as data:
                    data["test_code"] = message.text
                    button =  InlineKeyboardMarkup()
                    button_h = types.InlineKeyboardButton(text="начать тестирование", callback_data="start_test")
                    button.add(button_h)
                    button_h = types.InlineKeyboardButton(text="Назад", callback_data="start")
                    button.add(button_h)
                    await message.answer("Выберите вариант",reply_markup = button)
                await test_status.Q2.set()
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
async def passing_the_test2(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        test_code1 = data["test_code"]
    #проверка на наличия теста
    code = BotDB.get_test(test_code1)
    i = 0
    msg = []
    test_id = code[0]
    test_time = code[1]
    question = BotDB.get_question_test(test_id)
    user_id = BotDB.user_exists(call.from_user.id)
    a = BotDB.get_test_attempts(test_id)
    t = BotDB.get_test_result(user_id[0], test_id)
    len_test = BotDB.get_test_questions(test_id)
    user_and_test = [user_id[0], test_id]
    #проверка на повторное прохождение
    BotDB.test_result_add(user_id[0],test_id)
    #проверка режима работы теста рандомный и нет
    i1 = BotDB.get_test_random_mode(test_id)
    if i1[0] == 1:
        for s in random.sample(question,len(question)):
            right_otv = []
            all = "Вопрос:\n" + str(s[1])
            if len(BotDB.get_answer_test_right(s[0])) > 1:
                all = all + "\nВопрос с несколькими вариантами ответа"
            answers = BotDB.get_answer_test(s[0])
            if len(answers) != 0:
                i = 0
                button =  InlineKeyboardMarkup()
                answer_get = []
                for answer in random.sample(answers,len(answers)):
                    all = all + "\n" + chr(ord('a') + i) + ")" + str(answer[0])
                    button_h = types.InlineKeyboardButton(chr(ord('a') + i), callback_data = str(i))
                    answer_get.append(answer[2])
                    if answer[1] == 1:
                        right_otv.append(i)
                    i = i+1
                    button.add(button_h)
                button_h = types.InlineKeyboardButton("Далее", callback_data = "next")
                button.add(button_h)
                if s[2] != 0:
                    all = all + "\n Вопрос будет удален через " + str(s[2]) + " секунд"
                else:
                    all = all + "\n Вопрос будет удален через " + str(test_time) + " секунд"
                #добавление картинки к вопросу
                img = BotDB.get_question_test_pictures_id(s[0])
                photo = None
                if(img[0] != None):
                    photo = os.path.join(".","pictures",str(img[0])+".png")
                number_of_answer = len(answers)
                msg_a = all, button, right_otv, photo, s[0], answer_get, number_of_answer, s[2]
                msg.append(msg_a)
            else:
                img = BotDB.get_question_test_pictures_id(s[0])
                photo = None
                if(img[0] != None):
                    photo = os.path.join(".","pictures",str(img[0])+".png")
                all = all + "\nОтвет на вопрос необходимо написать"
                if s[2] != 0:
                    all = all + "\n Вопрос будет удален через " + str(s[2]) + " секунд"
                else:
                    all = all + "\n Вопрос будет удален через " + str(test_time) + " секунд"
                msg_a = all, s[0] ,photo, s[2]
                msg.append(msg_a)
    else:
        for s in question:
            right_otv = []
            all = "Вопрос:\n" + str(s[1])
            if len(BotDB.get_answer_test_right(s[0])) > 1:
                all = all + "\nВопрос с несколькими вариантами ответа"
            answers = BotDB.get_answer_test(s[0])
            if len(answers) != 0:
                i = 0
                button =  InlineKeyboardMarkup()
                answer_get = []
                for answer in random.sample(answers,len(answers)):
                    all = all + "\n" + chr(ord('a') + i) + ")" + str(answer[0])
                    button_h = types.InlineKeyboardButton(chr(ord('a') + i), callback_data = str(i))
                    answer_get.append(answer[2])
                    if answer[1] == 1:
                        right_otv.append(i)
                    i = i+1
                    button.add(button_h)
                button_h = types.InlineKeyboardButton("Далее", callback_data = "next")
                button.add(button_h)
                if s[2] != 0:
                    all = all + "\n Вопрос будет удален через " + str(s[2]) + " секунд"
                else:
                    all = all + "\n Вопрос будет удален через " + str(test_time) + " секунд"
                #добавление картинки к вопросу
                img = BotDB.get_question_test_pictures_id(s[0])
                photo = None
                if(img[0] != None):
                    photo = os.path.join(".","pictures",str(img[0])+".png")
                number_of_answer = len(answers)
                msg_a = all, button, right_otv, photo, s[0], answer_get, number_of_answer, s[2]
                msg.append(msg_a)
            else:
                img = BotDB.get_question_test_pictures_id(s[0])
                photo = None
                if(img[0] != None):
                    photo = os.path.join(".","pictures",str(img[0])+".png")
                all = all + "\nОтвет на вопрос необходимо написать"
                if s[2] != 0:
                    all = all + "\n Вопрос будет удален через " + str(s[2]) + " секунд"
                else:
                    all = all + "\n Вопрос будет удален через " + str(test_time) + " секунд"
                msg_a = all, s[0] ,photo, s[2]
                msg.append(msg_a)
    i = 0
    async with state.proxy() as data:
        data['user'] = user_and_test[0]
        data['test'] = user_and_test[1]
        data['msg'] = msg
        data['test_time'] = test_time
        data['i1'] = i1[0]
        data['i'] = i
        data['len_test'] = len_test[0]
        data['call_data'] = -1
        data['call_data_multiple_answers'] = []
    await passing_the_test3(call.message, state)
###################################################################################################################################
#прохождение теста
async def passing_the_test3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user = data['user']
        test = data['test']
        msg = data['msg']
        test_time = data['test_time']
        i = data['i']
        len_test = data['len_test']
        i1 = data['i1']
    #проверка на колличество вопросов
    if ((i == len(msg)) or ((i == len_test) and i1)):
        id2 = BotDB.get_test_result(user,test)
        id1 = id2[len(id2)-1][0]
        results = BotDB.get_question_result(id1)
        mark = BotDB.get_test_mark(test)
        sum = 0
        cost = 0
        mark1 = 0
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
        await message.answer(str(sum)+" правильных ответов из "+str(cost))
        await message.answer("Оценка: "+str(mark1))
        BotDB.test_result_add_result(str(sum)+"/"+str(cost), id1, mark1)
        await state.finish()
        await interface_all_begin(message, state)
    else:
        if len(msg[i]) != 4:
            #добавление фото
            if msg[i][3] != None:
                photo = open(msg[i][3], 'rb')
                msg1 = await message.answer_photo(photo, caption = msg[i][0], reply_markup = msg[i][1])
            else:
                msg1 = await message.answer(msg[i][0], reply_markup = msg[i][1])
            i=i+1
            async with state.proxy() as data:
                data['i'] = i
                data['msg1'] = msg1
            await test_status.Q3.set()
            if msg[i-1][7] != 0:
                asyncio.create_task(delete_message(state, msg1, msg[i-1][7]))
            else:
                asyncio.create_task(delete_message(state, msg1, test_time))
        else:
            if msg[i][2] != None:
                photo = open(msg[i][2], 'rb')
                msg1 = await message.answer_photo(photo, caption = msg[i][0])
            else:
                msg1 = await message.answer(msg[i][0])
            i=i+1
            async with state.proxy() as data:
                data['i'] = i
                data['msg1'] = msg1
            await test_status.Q4.set()
            if msg[i-1][3] != 0:
                asyncio.create_task(delete_message(state, msg1, msg[i-1][3], mode = 1))
            else:
                asyncio.create_task(delete_message(state, msg1, test_time, mode = 1))
###################################################################################################################################
#получает все CallbackQuery для ответа на тест
async def callbacks(call: types.CallbackQuery, state: FSMContext):
    call_data = call.data
    async with state.proxy() as data:
        msg = data['msg']
        i = data['i']
    if len(msg[i-1][2])==1:
        async with state.proxy() as data:
            data['call_data'] = call_data
        await update_message(call, state, call_data)
    else:
        async with state.proxy() as data:
            call_data_multiple_answers = data['call_data_multiple_answers']
        flag = 0
        c_helper = []
        for c in call_data_multiple_answers:
            if c == call_data:
                flag = 1
            else:
                c_helper.append(c)
        if flag == 0:
            c_helper.append(call_data)
        c_helper.sort()


        async with state.proxy() as data:
            data['call_data_multiple_answers'] = c_helper
        await update_message_multiple_answers(call, state, c_helper)
###################################################################################################################################
async def callbacks_next(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        call_data = data['call_data']
        user = data['user']
        test = data['test']
        msg = data['msg']
        msg1 = data['msg1']
        i = data['i']
        call_data_multiple_answers = data['call_data_multiple_answers']
    id2 = BotDB.get_test_result(user,test)
    id1 = id2[len(id2)-1][0]
    #проверка правильности ответа
    if len(msg[i-1][2]) == 1:
        if str(msg[i-1][2][0]) == call_data:
            BotDB.answer_question_result(id1,True,msg[i-1][4],msg[i-1][5][int(call_data)])
        else: 
            BotDB.answer_question_result(id1,False,msg[i-1][4],msg[i-1][5][int(call_data)])
    else:
        flag = 0
        if len(msg[i-1][2]) == len(call_data_multiple_answers):
            for j in range(len(msg[i-1][2]) - 1):
                if str(msg[i-1][2][j]) != call_data_multiple_answers[j]:
                    flag = 1
        else:
            flag = 1
        text = "multiple_answers:"
        for c in call_data_multiple_answers:
            text = text + ',' + str(msg[i-1][5][int(c)])
        if flag != 0:
            BotDB.answer_question_result_multiple_answers(id1,False,msg[i-1][4],text)
        else:
            BotDB.answer_question_result_multiple_answers(id1,True,msg[i-1][4],text)


    #удаление сообщения в случае ответа
    asyncio.create_task(delete_message(state, msg1, 0))
    await passing_the_test3(call.message, state)
###################################################################################################################################
async def text_response(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user = data['user']
        test = data['test']
        msg = data['msg']
        msg1 = data['msg1']
        i = data['i']
    id2 = BotDB.get_test_result(user,test)
    id1 = id2[len(id2)-1][0]
    #проверка правильности ответа
    BotDB.answer_question_result_text_response(id1, msg[i-1][1], message.text)
    #удаление сообщения в случае ответа
    asyncio.create_task(delete_message(state, msg1, 0, 1))
    await passing_the_test3(message, state)









def register_passing_the_test(dp: Dispatcher):
    dp.register_callback_query_handler(passing_the_test, lambda c: c.data == "passing_the_test")
    dp.register_message_handler(passing_the_test1, content_types = ['text'], state=test_status.Q1)
    dp.register_callback_query_handler(passing_the_test2,lambda c: c.data == "start_test", state=test_status.Q2)
    dp.register_callback_query_handler(callbacks_next, lambda c: c.data == "next", state=test_status.Q3)
    dp.register_callback_query_handler(callbacks, state=test_status.Q3)
    dp.register_message_handler(text_response,content_types = ['text'], state=test_status.Q4)