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
from tgbot.misc.states import test_status_v2,all
from tgbot.handlers.interface_all import interface_all_begin, interface_all_begin4
import random
#ошибки 6000
time_update = 5 #частота обновления таймера

#класс для переменной теста
class test(object):
    def __init__(self):
        #тип вопроса
        self.type = None    #"text","one_answer","many_answers"
        #код вопроса
        self.question_code = None
        #текст вопроса
        self.text_question = None
        #переменная с кнопками
        self.button = None
        #номер правильного ответа
        self.correct_answer_number = None
        #код фото
        self.photo_code = None
        #все варианты ответа
        self.all_response_options = None
        #время ответа(оставшееся время)
        self.response_time = None
        #выбранный(е) вариант ответа
        self.selected_answer_option = None
        #текстовый ответ на вопрос
        self.text_response = None


###################################################################################################################################
async def update_message_time(state: FSMContext):
    pass
###################################################################################################################################
async def update_message(call: types.CallbackQuery, state: FSMContext, call_data):
    pass
###################################################################################################################################
async def update_message_multiple_answers(call: types.CallbackQuery, state: FSMContext, call_data_multiple_answers):
    pass
###################################################################################################################################
#удаление сообщений через определенное время
async def delete_message(state: FSMContext, message: types.Message, sleep_time: int = 0, mode: int = 0, id_ovet: int = -1):
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
        question = BotDB.get_question_test(test_id)
        title, a, i1, len_test = BotDB.get_test_title_attempts_random_mode_questions(test_id)
        t = BotDB.get_test_result(user_id[0], test_id)
        #вывод информации о тесте
        await message.answer("Название теста: "+str(title[0][:-1]))
        await message.answer("Количество попыток: "+str(a[0]))
        await message.answer("Количество использованных попыток: "+str(len(t)))
        if i1[0]:   #при не случайном выборе вопросов не указывается количество вопросов
            await message.answer("Количество вопросов: "+str(len_test[0]))
        else:
            await message.answer("Количество вопросов: "+str(len(question)))
        #проверка на активировнн ли тест
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
async def passing_the_test2(call: types.CallbackQuery, state: FSMContext):
    pass
###################################################################################################################################
#прохождение теста
async def passing_the_test3(message: types.Message, state: FSMContext):
    pass
###################################################################################################################################
#получает все CallbackQuery для ответа на тест
async def callbacks(call: types.CallbackQuery, state: FSMContext):
    pass
###################################################################################################################################
async def callbacks_next(call: types.CallbackQuery, state: FSMContext):
    pass
###################################################################################################################################
async def callbacks_next_text_response(call: types.CallbackQuery, state: FSMContext):
    pass
###################################################################################################################################
async def callbacks_prev(call: types.CallbackQuery, state: FSMContext):
    pass
###################################################################################################################################
async def callbacks_prev_text_response(call: types.CallbackQuery, state: FSMContext):
    pass
###################################################################################################################################
async def text_response(message: types.Message, state: FSMContext):
    pass
        



def register_passing_the_test_v2(dp: Dispatcher):
    dp.register_callback_query_handler(code_request, lambda c: c.data == "passing_the_test_v2", state=all.interface_all_stateQ1)
    dp.register_message_handler(output_information_about_test, content_types = ['text'], state=test_status_v2.Q1)
    dp.register_callback_query_handler(passing_the_test2,lambda c: c.data == "start_test", state=test_status_v2.Q2)
    dp.register_message_handler(text_response,content_types = ['text'], state=test_status_v2.Q4)
    dp.register_callback_query_handler(callbacks_next, lambda c: c.data == "next", state=test_status_v2.Q3)
    dp.register_callback_query_handler(callbacks_prev, lambda c: c.data == "prev", state=test_status_v2.Q3)
    dp.register_callback_query_handler(callbacks_next_text_response, lambda c: c.data == "next", state=test_status_v2.Q4)
    dp.register_callback_query_handler(callbacks_prev_text_response, lambda c: c.data == "prev", state=test_status_v2.Q4)
    dp.register_callback_query_handler(callbacks, state=test_status_v2.Q3)