import os.path
import datetime
import asyncio
from aiogram.utils.exceptions import MessageNotModified
from contextlib import suppress
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import (MessageCantBeDeleted, MessageToDeleteNotFound, )
from aiogram.types import InlineKeyboardMarkup
from tgbot.middlewares.DBhelp import BotDB
from tgbot.misc.states import test_status,all
from tgbot.handlers.interface_all import interface_all_begin, interface_all_begin4
import random
#ошибки 6000
time_update = 5 #частота обновления таймера


###################################################################################################################################
async def update_message_time(state: FSMContext):
    try:
        async with state.proxy() as data:
            i = data['i']
            msg = data['msg']
            msg1 = data["msg1"]
        while True:
            try:
                await asyncio.sleep(time_update)
                button =  InlineKeyboardMarkup()
                if len(msg[i-1]) > 5:
                    if len(msg[i-1][2]) == 1:
                        async with state.proxy() as data:
                            time = data['time']
                            call_data = data['call_data']
                        for j in range(msg[i-1][6]):
                            if int(call_data) != j :
                                button_h = types.InlineKeyboardButton(chr(ord('a') + j), callback_data = str(j))
                                button.add(button_h)
                            else:
                                button_h = types.InlineKeyboardButton("[" + chr(ord('a') + j) + "]", callback_data = str(j))
                                button.add(button_h)
                    else:
                        async with state.proxy() as data:
                            time = data['time']
                            call_data_multiple_answers = data['call_data_multiple_answers']
                        j1 = 0
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
                if len(msg)-1 == i:
                    button_h_1 = types.InlineKeyboardButton("Назад", callback_data = "prev")
                    button_h_2 = types.InlineKeyboardButton("Закончить тест", callback_data = "next")
                    button.row(button_h_1, button_h_2)
                else:
                    flag = 0
                    for ji in range(i-1):
                        if (len(msg[ji]) == 8) or (len(msg[ji]) == 9):
                            if msg[ji][7] != 0:
                                flag = 1
                        elif (len(msg[ji]) == 4) or (len(msg[ji]) == 5):
                            if msg[ji][3] != 0:
                                flag = 1
                    if flag == 1:
                        button_h_1 = types.InlineKeyboardButton("Назад", callback_data = "prev")
                        button_h_2 = types.InlineKeyboardButton("Далее", callback_data = "next")
                        button.row(button_h_1, button_h_2)
                    else:
                        button_h_2 = types.InlineKeyboardButton("Далее", callback_data = "next")
                        button.add(button_h_2)
                async with state.proxy() as data:
                    time = data['time']
                time_2 = datetime.datetime.now() - time
                if len(msg[i-1]) > 5:
                    button_h = types.InlineKeyboardButton("Осталось времени: " + str(int(msg[i-1][7]) - int(time_2.total_seconds())) + "c", callback_data = "None")
                else:
                    button_h = types.InlineKeyboardButton("Осталось времени: " + str(int(msg[i-1][3]) - int(time_2.total_seconds())) + "c", callback_data = "None")
                button.add(button_h)
                await msg1.edit_reply_markup(reply_markup=button)
            except MessageNotModified:
                pass
    except:
        pass
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
        
        if len(msg)-1 == i:
            button_h_1 = types.InlineKeyboardButton("Назад", callback_data = "prev")
            button_h_2 = types.InlineKeyboardButton("Закончить тест", callback_data = "next")
            button.row(button_h_1, button_h_2)
        else:
            flag = 0
            for ji in range(i-1):
                if (len(msg[ji]) == 8) or (len(msg[ji]) == 9):
                    if msg[ji][7] != 0:
                        flag = 1
                elif (len(msg[ji]) == 4) or (len(msg[ji]) == 5):
                    if msg[ji][3] != 0:
                        flag = 1
            if flag == 1:
                button_h_1 = types.InlineKeyboardButton("Назад", callback_data = "prev")
                button_h_2 = types.InlineKeyboardButton("Далее", callback_data = "next")
                button.row(button_h_1, button_h_2)
            else:
                button_h_2 = types.InlineKeyboardButton("Далее", callback_data = "next")
                button.add(button_h_2)
        async with state.proxy() as data:
            time = data['time']
        time_2 = datetime.datetime.now() - time
        button_h = types.InlineKeyboardButton("Осталось времени: " + str(int(msg[i-1][7]) - int(time_2.total_seconds())) + "c", callback_data = "None")
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
        if len(msg)-1 == i:
            button_h_1 = types.InlineKeyboardButton("Назад", callback_data = "prev")
            button_h_2 = types.InlineKeyboardButton("Закончить тест", callback_data = "next")
            button.row(button_h_1, button_h_2)
        else:
            flag = 0
            for ji in range(i-1):
                if (len(msg[ji]) == 8) or (len(msg[ji]) == 9):
                    if msg[ji][7] != 0:
                        flag = 1
                elif (len(msg[ji]) == 4) or (len(msg[ji]) == 5):
                    if msg[ji][3] != 0:
                        flag = 1
            if flag == 1:
                button_h_1 = types.InlineKeyboardButton("Назад", callback_data = "prev")
                button_h_2 = types.InlineKeyboardButton("Далее", callback_data = "next")
                button.row(button_h_1, button_h_2)
            else:
                button_h_2 = types.InlineKeyboardButton("Далее", callback_data = "next")
                button.add(button_h_2)
        async with state.proxy() as data:
            time = data['time']
        time_2 = datetime.datetime.now() - time
        button_h = types.InlineKeyboardButton("Осталось времени: " + str(int(msg[i-1][7]) - int(time_2.total_seconds())) + "c", callback_data = "None")
        button.add(button_h)
        await call.message.edit_reply_markup(reply_markup=button)
    except:
        pass
###################################################################################################################################
#удаление сообщений через определенное время
async def delete_message(state: FSMContext, message: types.Message, sleep_time: int = 0, mode: int = 0, id_ovet: int = -1):
    try:
        async with state.proxy() as data:
            msg = data['msg']
            msg1 = data['msg1']
            i = data['i']
        await asyncio.sleep(sleep_time)
        with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        
            if sleep_time != 0: 
                async with state.proxy() as data:
                    user = data['user']
                    test = data['test']
                    call_data = data['call_data']
                await msg1.delete()
                id1 = BotDB.get_test_result(user, test)
                if mode == 0:
                    if (call_data == -1) and ((len(msg[i-1]) == 8) or (len(msg[i-1]) == 4)):
                        BotDB.answer_question_result2(id1[len(id1)-1][0],False,msg[i-1][4])
                    elif(len(msg[i-1]) == 8) or (len(msg[i-1]) == 4):
                        async with state.proxy() as data:
                            user = data['user']
                            test = data['test']
                            msg = data['msg']
                            i = data['i']
                        id2 = BotDB.get_test_result(user,test)
                        id1 = id2[len(id2)-1][0]
                        #проверка правильности ответа
                        if (str(msg[i-1][2][0]) == call_data) and ((len(msg[i-1]) == 8) or (len(msg[i-1]) == 4)):
                            BotDB.answer_question_result(id1,True,msg[i-1][4],msg[i-1][5][int(call_data)])
                        elif (msg[i-1] == 8) or (msg[i-1] == 4): 
                            BotDB.answer_question_result(id1,False,msg[i-1][4],msg[i-1][5][int(call_data)])
                        async with state.proxy() as data:
                            data['call_data'] = -1
                elif (len(msg[i-1]) == 8) or (len(msg[i-1]) == 4):
                    BotDB.answer_question_result_text_response(id1[len(id1)-1][0],msg[i-1][1],"None")
                if (len(msg[i-1]) == 8) or (len(msg[i-1]) == 9):
                    msg[i-1] =  msg[i-1][0], msg[i-1][1], msg[i-1][2],  msg[i-1][3], msg[i-1][4], msg[i-1][5], msg[i-1][6], 0, 0
                else:
                    msg[i-1] = msg[i-1][0], msg[i-1][1], msg[i-1][2], 0, 0
                async with state.proxy() as data:
                    data['msg'] = msg
                await passing_the_test3(message, state)
            else:
                async with state.proxy() as data:
                    time = data['time']
                    i = data['i']
                time_2 = datetime.datetime.now() - time
                await msg1.delete()
                if (id_ovet != -1):
                    if (len(msg[i-1]) == 8) or (len(msg[i-1]) == 9):
                        msg[i-1] =  msg[i-1][0], msg[i-1][1], msg[i-1][2],  msg[i-1][3], msg[i-1][4], msg[i-1][5], msg[i-1][6], int(msg[i-1][7]) - int(time_2.total_seconds()), id_ovet
                    else:
                        msg[i-1] = msg[i-1][0], msg[i-1][1], msg[i-1][2], int(msg[i-1][3]) - int(time_2.total_seconds()), id_ovet
                else:
                    if (len(msg[i-1]) == 8) or (len(msg[i-1]) == 9):
                        msg[i-1] =  msg[i-1][0], msg[i-1][1], msg[i-1][2],  msg[i-1][3], msg[i-1][4], msg[i-1][5], msg[i-1][6], int(msg[i-1][7]) - int(time_2.total_seconds()), msg[i-1][8]
                    else:
                        msg[i-1] = msg[i-1][0], msg[i-1][1], msg[i-1][2], int(msg[i-1][3]) - int(time_2.total_seconds()), msg[i-1][4]
                async with state.proxy() as data:
                    data['msg'] = msg
    except:
        pass
###################################################################################################################################
#вспомогательная
async def passing_the_test(call: types.CallbackQuery, state: FSMContext):
    try:
        button =  InlineKeyboardMarkup()
        button_h = types.InlineKeyboardButton(("Отмена"), callback_data = "start")
        button.add(button_h)
        await call.message.answer("Введите код теста", reply_markup = button)
        await test_status.Q1.set()
    except:
        await call.message.answer("Произошла ошибка 6001")
        await state.finish()
###################################################################################################################################
async def passing_the_test1(message: types.Message, state: FSMContext):
    try:
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
                        button_h = types.InlineKeyboardButton(text="Начать тестирование", callback_data="start_test")
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
    except:
        await message.answer("Произошла ошибка 6002")
        await state.finish()
###################################################################################################################################
#создает переменную с тестом
async def passing_the_test2(call: types.CallbackQuery, state: FSMContext):
    try:
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
                    all = all + "\n\nВопрос с несколькими вариантами ответа"
                elif len(BotDB.get_answer_test_right(s[0])) == 1:
                    all = all + "\n\nВопрос с одним вариантом ответа"
                answers = BotDB.get_answer_test(s[0])
                if len(answers) != 0:
                    i = 0
                    button =  InlineKeyboardMarkup()
                    answer_get = []
                    for answer in random.sample(answers,len(answers)):
                        all = all + "\n" + chr(ord('a') + i) + ") " + str(answer[0])
                        button_h = types.InlineKeyboardButton(chr(ord('a') + i), callback_data = str(i))
                        answer_get.append(answer[2])
                        if answer[1] == 1:
                            right_otv.append(i)
                        i = i+1
                        button.add(button_h)
                    #добавление картинки к вопросу
                    img = BotDB.get_question_test_pictures_id(s[0])
                    photo = None
                    if(img[0] != None):
                        photo = os.path.join(".","pictures",str(img[0])+".png")
                    number_of_answer = len(answers)
                    if s[2] != 0:
                        msg_a = all, button, right_otv, photo, s[0], answer_get, number_of_answer, s[2]
                    else:
                        msg_a = all, button, right_otv, photo, s[0], answer_get, number_of_answer, test_time
                    msg.append(msg_a)
                else:
                    img = BotDB.get_question_test_pictures_id(s[0])
                    photo = None
                    if(img[0] != None):
                        photo = os.path.join(".","pictures",str(img[0])+".png")
                    all = all + "\n\nОтвет на вопрос необходимо написать"
                    if s[2] != 0:
                        msg_a = all, s[0] ,photo, s[2]
                    else:
                        msg_a = all, s[0] ,photo, test_time
                    msg.append(msg_a)
        else:
            for s in question:
                right_otv = []
                all = "Вопрос:\n" + str(s[1])
                if len(BotDB.get_answer_test_right(s[0])) > 1:
                    all = all + "\n\nВопрос с несколькими вариантами ответа"
                elif len(BotDB.get_answer_test_right(s[0])) == 1:
                    all = all + "\n\nВопрос с одним вариантом ответа"
                answers = BotDB.get_answer_test(s[0])
                if len(answers) != 0:
                    i = 0
                    button =  InlineKeyboardMarkup()
                    answer_get = []
                    for answer in random.sample(answers,len(answers)):
                        all = all + "\n" + chr(ord('a') + i) + ") " + str(answer[0])
                        button_h = types.InlineKeyboardButton(chr(ord('a') + i), callback_data = str(i))
                        answer_get.append(answer[2])
                        if answer[1] == 1:
                            right_otv.append(i)
                        i = i+1
                        button.add(button_h)
                    #добавление картинки к вопросу
                    img = BotDB.get_question_test_pictures_id(s[0])
                    photo = None
                    if(img[0] != None):
                        photo = os.path.join(".","pictures",str(img[0])+".png")
                    number_of_answer = len(answers)
                    if s[2] != 0:
                        msg_a = all, button, right_otv, photo, s[0], answer_get, number_of_answer, s[2]
                    else:
                        msg_a = all, button, right_otv, photo, s[0], answer_get, number_of_answer, test_time
                    msg.append(msg_a)
                else:
                    img = BotDB.get_question_test_pictures_id(s[0])
                    photo = None
                    if(img[0] != None):
                        photo = os.path.join(".","pictures",str(img[0])+".png")
                    all = all + "\n\nОтвет на вопрос необходимо написать"
                    if s[2] != 0:
                        msg_a = all, s[0] ,photo, s[2]
                    else:
                        msg_a = all, s[0] ,photo, test_time
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
    except:
        await call.message.answer("Произошла ошибка 6003")
        await state.finish()
###################################################################################################################################
#прохождение теста
async def passing_the_test3(message: types.Message, state: FSMContext):
    try:
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
            if mark[1] == 0 and mark[0] == 0 and mark[2] == 0:
                await message.answer("Тест пройден")
                BotDB.test_result_add_result("Тест пройден", id1, "None")
            elif mark[1] == 0 and mark[0] == 0 and mark[2] != 0:
                for r in results:
                    if r[0] != None:
                        sum = sum + r[0]
                        cost = cost + 1
                await message.answer(str(sum)+" правильных ответов из "+str(cost))
                if int(mark[2]) <= sum:
                    await message.answer("Тест сдан")
                    BotDB.test_result_add_result(str(sum)+"/"+str(cost), id1, "Тест сдан")
                else:
                    await message.answer("Тест не сдан")
                    BotDB.test_result_add_result(str(sum)+"/"+str(cost), id1, "Тест не сдан")
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
                await message.answer(str(sum)+" правильных ответов из "+str(cost))
                await message.answer("Оценка: "+str(mark1))
                BotDB.test_result_add_result(str(sum)+"/"+str(cost), id1, mark1)
            await state.finish()
            await interface_all_begin4(message, state)
        else:
            if (len(msg[i]) == 8) or (len(msg[i]) == 9):
                button = msg[i][1]
                if len(msg)-2 == i:
                    button_h_1 = types.InlineKeyboardButton("Назад", callback_data = "prev")
                    button_h_2 = types.InlineKeyboardButton("Закончить тест", callback_data = "next")
                    button.row(button_h_1, button_h_2)
                else:
                    flag = 0
                    for ji in range(i):
                        if (len(msg[ji]) == 8) or (len(msg[ji]) == 9):
                            if msg[ji][7] != 0:
                                flag = 1
                        elif (len(msg[ji]) == 4) or (len(msg[ji]) == 5):
                            if msg[ji][3] != 0:
                                flag = 1
                    if flag == 1:
                        button_h_1 = types.InlineKeyboardButton("Назад", callback_data = "prev")
                        button_h_2 = types.InlineKeyboardButton("Далее", callback_data = "next")
                        button.row(button_h_1, button_h_2)
                    else:
                        button_h_2 = types.InlineKeyboardButton("Далее", callback_data = "next")
                        button.add(button_h_2)
                text = msg[i][0]
                if msg[i][7] != 0:
                    button_h = types.InlineKeyboardButton("Осталось времени: " + str(int(msg[i][7])) + "c", callback_data = "None")
                    text = text + "\n Вопрос будет удален через " + str(msg[i][7]) + " секунд"
                else:
                    button_h = types.InlineKeyboardButton("Осталось времени: " + str(int(test_time)) + "c", callback_data = "None")
                    text = text + "\n Вопрос будет удален через " + str(test_time) + " секунд"
                button.add(button_h)
                #добавление фото
                if msg[i][3] != None:
                    photo = open(msg[i][3], 'rb')
                    msg1 = await message.answer_photo(photo, caption = text, reply_markup = button)
                else:
                    msg1 = await message.answer(text, reply_markup = button)
                i=i+1
                async with state.proxy() as data:
                    data['i'] = i
                    data['msg1'] = msg1
                    data['call_data'] = -1
                    data['call_data_multiple_answers'] = []
                await test_status.Q3.set()
                asyncio.create_task(update_message_time(state))
                if msg[i-1][7] != 0:
                    asyncio.create_task(delete_message(state, msg1, msg[i-1][7]))
                else:
                    asyncio.create_task(delete_message(state, msg1, test_time))
                time = datetime.datetime.now()
                async with state.proxy() as data:
                    data['time'] = time
            elif (len(msg[i]) == 4) or (len(msg[i]) == 5):
                button =  InlineKeyboardMarkup()
                if len(msg)-2 == i:
                    button_h_1 = types.InlineKeyboardButton("Назад", callback_data = "prev")
                    button_h_2 = types.InlineKeyboardButton("Закончить тест", callback_data = "next")
                    button.row(button_h_1, button_h_2)
                else:
                    flag = 0
                    for ji in range(i):
                        if (len(msg[ji]) == 8) or (len(msg[ji]) == 9):
                            if msg[ji][7] != 0:
                                flag = 1
                        elif (len(msg[ji]) == 4) or (len(msg[ji]) == 5):
                            if msg[ji][3] != 0:
                                flag = 1
                    if flag == 1:
                        button_h_1 = types.InlineKeyboardButton("Назад", callback_data = "prev")
                        button_h_2 = types.InlineKeyboardButton("Далее", callback_data = "next")
                        button.row(button_h_1, button_h_2)
                    else:
                        button_h_2 = types.InlineKeyboardButton("Далее", callback_data = "next")
                        button.add(button_h_2)
                text = msg[i][0]
                if msg[i][3] != 0:
                    button_h = types.InlineKeyboardButton("Осталось времени: " + str(msg[i][3]) + "c", callback_data = "None")
                    text = text + "\n Вопрос будет удален через " + str(msg[i][3]) + " секунд"
                else:
                    button_h = types.InlineKeyboardButton("Осталось времени: " + str(test_time) + "c", callback_data = "None")
                    text = text + "\n Вопрос будет удален через " + str(test_time) + " секунд"
                button.add(button_h)
                if msg[i][2] != None:
                    photo = open(msg[i][2], 'rb')
                    msg1 = await message.answer_photo(photo, caption = text, reply_markup = button)
                else:
                    msg1 = await message.answer(text, reply_markup = button)
                i=i+1
                async with state.proxy() as data:
                    data['i'] = i
                    data['msg1'] = msg1
                    data['call_data'] = -1
                    data['call_data_multiple_answers'] = []
                await test_status.Q4.set()
                asyncio.create_task(update_message_time(state))
                if msg[i-1][3] != 0:
                    asyncio.create_task(delete_message(state, msg1, msg[i-1][3], mode = 1))
                else:
                    asyncio.create_task(delete_message(state, msg1, test_time, mode = 1))
                time = datetime.datetime.now()
                async with state.proxy() as data:
                    data['time'] = time
    except:
        await message.answer("Произошла ошибка 6004")
        await state.finish()
###################################################################################################################################
#получает все CallbackQuery для ответа на тест
async def callbacks(call: types.CallbackQuery, state: FSMContext):
    try:
        flag = 1
        try:
            int(call.data)
        except:
            flag = 0
        if flag == 1:
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
        else:
            pass
    except:
        await call.message.answer("Произошла ошибка 6005")
        await state.finish()
###################################################################################################################################
async def callbacks_next(call: types.CallbackQuery, state: FSMContext):
    try:
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
        id = 0
        if (len(msg[i-1][2]) == 1) and (len(msg[i-1]) == 8):
            if str(msg[i-1][2][0]) == call_data:
                id = BotDB.answer_question_result(id1,True,msg[i-1][4],msg[i-1][5][int(call_data)])
            else: 
                id = BotDB.answer_question_result(id1,False,msg[i-1][4],msg[i-1][5][int(call_data)])
        elif (len(msg[i-1][2]) > 1) and (len(msg[i-1]) == 8):
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
                id = BotDB.answer_question_result_multiple_answers(id1,False,msg[i-1][4],text)
            else:
                id = BotDB.answer_question_result_multiple_answers(id1,True,msg[i-1][4],text)
        elif (len(msg[i-1][2]) == 1) and (len(msg[i-1]) == 9):
            if str(msg[i-1][2][0]) == call_data:
                BotDB.answer_question_result_update(msg[i-1][8], id1,True,msg[i-1][4],msg[i-1][5][int(call_data)])
            else: 
                BotDB.answer_question_result_update(msg[i-1][8], id1,False,msg[i-1][4],msg[i-1][5][int(call_data)])
        elif (len(msg[i-1][2]) > 1) and (len(msg[i-1]) == 9):
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
                BotDB.answer_question_result_multiple_answers_update(msg[i-1][8], id1,False,msg[i-1][4],text)
            else:
                BotDB.answer_question_result_multiple_answers_update(msg[i-1][8], id1,True,msg[i-1][4],text)

        #удаление сообщения в случае ответа
        if (len(msg[i-1]) == 8) or (len(msg[i-1]) == 4):
            await delete_message(state, msg1, 0, 0, id_ovet = id)
        elif (len(msg[i-1]) == 9) or (len(msg[i-1]) == 5):
            await delete_message(state, msg1, 0, 0)
        ji = -1
        for j in range(len(msg)):
            if ((len(msg[j]) == 8) or (len(msg[j]) == 9)) and (i - 1 < j) and (ji == -1):
                if msg[j][7] != 0:
                    ji = j
            elif ((len(msg[j]) == 4) or (len(msg[j]) == 5)) and (i - 1 < j) and (ji == -1):
                if msg[j][3] != 0:
                    ji = j
        if ji != -1:
            async with state.proxy() as data:
                data['i'] = ji
        await passing_the_test3(call.message, state)
    except:
        await call.message.answer("Произошла ошибка 6006")
        await state.finish()
###################################################################################################################################
async def callbacks_next_text_response(call: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            user = data['user']
            test = data['test']
            msg = data['msg']
            msg1 = data['msg1']
            i = data['i']
        id2 = BotDB.get_test_result(user,test)
        id1 = id2[len(id2)-1][0]
        if len(msg[i-1]) == 4:
            id = BotDB.answer_question_result_text_response(id1,msg[i-1][1],"None")
            await delete_message(state, msg1, 0, 0, id_ovet = id)
        elif len(msg[i-1]) == 5:
            await delete_message(state, msg1, 0, 0)
        #удаление сообщения в случае ответа
        if (len(msg[i-1]) == 8) or (len(msg[i-1]) == 4):
            await delete_message(state, msg1, 0, 0, id_ovet = id)
        elif (len(msg[i-1]) == 9) or (len(msg[i-1]) == 5):
            await delete_message(state, msg1, 0, 0)
        ji = -1
        for j in range(len(msg)):
            if ((len(msg[j]) == 8) or (len(msg[j]) == 9)) and (i - 1 < j) and (ji == -1):
                if msg[j][7] != 0:
                    ji = j
            elif ((len(msg[j]) == 4) or (len(msg[j]) == 5)) and (i - 1 < j) and (ji == -1):
                if msg[j][3] != 0:
                    ji = j
        if ji != -1:
            async with state.proxy() as data:
                data['i'] = ji
        await passing_the_test3(call.message, state)
    except:
        await call.message.answer("Произошла ошибка 6007")
        await state.finish()
###################################################################################################################################
async def callbacks_prev(call: types.CallbackQuery, state: FSMContext):
    try:
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
        id = 0
        if (len(msg[i-1][2]) == 1) and (len(msg[i-1]) == 8):
            if str(msg[i-1][2][0]) == call_data:
                id = BotDB.answer_question_result(id1,True,msg[i-1][4],msg[i-1][5][int(call_data)])
            else: 
                id = BotDB.answer_question_result(id1,False,msg[i-1][4],msg[i-1][5][int(call_data)])
        elif (len(msg[i-1][2]) > 1) and (len(msg[i-1]) == 8):
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
                id = BotDB.answer_question_result_multiple_answers(id1,False,msg[i-1][4],text)
            else:
                id = BotDB.answer_question_result_multiple_answers(id1,True,msg[i-1][4],text)
        elif (len(msg[i-1][2]) == 1) and (len(msg[i-1]) == 9):
            if str(msg[i-1][2][0]) == call_data:
                BotDB.answer_question_result_update(msg[i-1][8], id1,True,msg[i-1][4],msg[i-1][5][int(call_data)])
            else: 
                BotDB.answer_question_result_update(msg[i-1][8], id1,False,msg[i-1][4],msg[i-1][5][int(call_data)])
        elif (len(msg[i-1][2]) > 1) and (len(msg[i-1]) == 9):
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
                BotDB.answer_question_result_multiple_answers_update(msg[i-1][8], id1,False,msg[i-1][4],text)
            else:
                BotDB.answer_question_result_multiple_answers_update(msg[i-1][8], id1,True,msg[i-1][4],text)

                #удаление сообщения в случае ответа
        if (len(msg[i-1]) == 8) or (len(msg[i-1]) == 4):
            await delete_message(state, msg1, 0, 0, id_ovet = id)
        elif (len(msg[i-1]) == 9) or (len(msg[i-1]) == 5):
            await delete_message(state, msg1, 0, 0)
        ji = -1
        for j in range(i-1):
            if (len(msg[j]) == 8) or (len(msg[j]) == 9):
                if msg[j][7] != 0:
                    ji = j
            elif (len(msg[j]) == 4) or (len(msg[j]) == 5):
                if msg[j][3] != 0:
                    ji = j
        if ji != -1:
            async with state.proxy() as data:
                data['i'] = ji
        await passing_the_test3(call.message, state)
    except:
        await call.message.answer("Произошла ошибка 6008")
        await state.finish()
###################################################################################################################################
async def callbacks_prev_text_response(call: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            user = data['user']
            test = data['test']
            msg = data['msg']
            msg1 = data['msg1']
            i = data['i']
        id2 = BotDB.get_test_result(user,test)
        id1 = id2[len(id2)-1][0]
        if len(msg[i-1]) == 4:
            id = BotDB.answer_question_result_text_response(id1,msg[i-1][1],"None")
            await delete_message(state, msg1, 0, 0, id_ovet = id)
        elif len(msg[i-1]) == 5:
            await delete_message(state, msg1, 0, 0)
        #удаление сообщения в случае ответа
        if (len(msg[i-1]) == 8) or (len(msg[i-1]) == 4):
            await delete_message(state, msg1, 0, 0, id_ovet = id)
        elif (len(msg[i-1]) == 9) or (len(msg[i-1]) == 5):
            await delete_message(state, msg1, 0, 0)
        ji = -1
        for j in range(i-1):
            if (len(msg[j]) == 8) or (len(msg[j]) == 9):
                if msg[j][7] != 0:
                    ji = j
            elif (len(msg[j]) == 4) or (len(msg[j]) == 5):
                if msg[j][3] != 0:
                    ji = j
        if ji != -1:
            async with state.proxy() as data:
                data['i'] = ji
        await passing_the_test3(call.message, state)
    except:
        await call.message.answer("Произошла ошибка 6009")
        await state.finish()
###################################################################################################################################
async def text_response(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            user = data['user']
            test = data['test']
            msg = data['msg']
            msg1 = data['msg1']
            i = data['i']
        id2 = BotDB.get_test_result(user,test)
        id1 = id2[len(id2)-1][0]
        #проверка правильности ответа
        if len(msg[i-1]) == 4:
            id = BotDB.answer_question_result_text_response(id1, msg[i-1][1], message.text)
            asyncio.create_task(delete_message(state, msg1, 0, 1, id))
        elif len(msg[i-1]) == 5:
            BotDB.answer_question_result_text_response_update(msg[i-1][4], message.text)
            asyncio.create_task(delete_message(state, msg1, 0, 1))
        #удаление сообщения в случае ответа
        await passing_the_test3(message, state)
    except:
        await message.answer("Произошла ошибка 6010")
        await state.finish()
        



def register_passing_the_test(dp: Dispatcher):
    dp.register_callback_query_handler(passing_the_test, lambda c: c.data == "passing_the_test", state=all.interface_all_stateQ1)
    dp.register_message_handler(passing_the_test1, content_types = ['text'], state=test_status.Q1)
    dp.register_callback_query_handler(passing_the_test2,lambda c: c.data == "start_test", state=test_status.Q2)
    dp.register_message_handler(text_response,content_types = ['text'], state=test_status.Q4)
    dp.register_callback_query_handler(callbacks_next, lambda c: c.data == "next", state=test_status.Q3)
    dp.register_callback_query_handler(callbacks_prev, lambda c: c.data == "prev", state=test_status.Q3)
    dp.register_callback_query_handler(callbacks_next_text_response, lambda c: c.data == "next", state=test_status.Q4)
    dp.register_callback_query_handler(callbacks_prev_text_response, lambda c: c.data == "prev", state=test_status.Q4)
    dp.register_callback_query_handler(callbacks, state=test_status.Q3)