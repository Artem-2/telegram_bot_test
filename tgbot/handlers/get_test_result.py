import asyncio
import xlwt
import os
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from tgbot.middlewares.DBhelp import BotDB
from tgbot.misc.states import get_test
from aiogram.types import InlineKeyboardMarkup
from tgbot.handlers.interface_all import interface_all_begin2
    





async def get_test_result(call: types.CallbackQuery):
    Title_Test_code = BotDB.get_test_title_test_code_no_active_mode(call.from_user.id)
    button =  InlineKeyboardMarkup()
    all = "Тесты данные о которых вы можете получить\n"
    for a in Title_Test_code:
        all = all + "\n" + "Код теста: " + a[1] + "\n" + "Название теста: " + a[0]
        button_h = types.InlineKeyboardButton((a[1]), callback_data = a[1])
        button.add(button_h)
    button_h = types.InlineKeyboardButton(("Отмена"), callback_data = "start")
    button.add(button_h)
    await call.message.answer(all, reply_markup = button)
    await get_test.Q1.set()


async def get_test_result2(call: types.CallbackQuery, state: FSMContext):
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Python Sheet 1") 
    sheet1.write(0, 0, "№")
    sheet1.write(0, 1, "Группа")
    sheet1.write(0, 2, "Фамилия Имя")
    sheet1.write(0, 3, "Количество верных ответов/общее количество ответов")
    sheet1.write(0, 4, "Оценка")
    sheet1.write(0, 5, "Дата прохождения теста")
    test_id = BotDB.get_test_user_create_id(int(call.from_user.id), str(call.data))
    questions = BotDB.get_question_test(test_id[0][0])
    i = 6
    for question in questions:
        sheet1.write(0, i, question[1])
        i = i + 1
    res = BotDB.get_test_result_all(test_id[0][0])
    i = 1
    for r in res:
        user_id = r[0]
        user_date = BotDB.get_user(user_id)
        sheet1.write(i, 0, i)
        sheet1.write(i, 1, user_date[1])
        sheet1.write(i, 2, user_date[0])
        sheet1.write(i, 3, r[1])
        sheet1.write(i, 4, r[2])
        sheet1.write(i, 5, r[3])
        id_question_id_answer = BotDB.get_question_result_id_question_id_answer_text_response(r[4])
        id_question_id_answer = sorted(id_question_id_answer, reverse=False, key=lambda x: x[0])
        for ii in id_question_id_answer:
            j = 6
            for question in questions:
                if question[0] == ii[0]:
                    answer = BotDB.get_answer_test_answer(ii[1])
                    if answer != None:
                            sheet1.write(i, j, answer[0])
                    else:
                        if ii[2] != None:
                            if ii[2].startswith("multiple_answers:,"):
                                result = ""
                                text = ii[2]
                                text = text.replace("multiple_answers:,","")
                                text = text.split(",")
                                for t in text:
                                    answer_in = BotDB.get_answer_test_answer(int(t))
                                    result = result + answer_in[0] + ","
                                sheet1.write(i, j, result)
                            elif ii[2].startswith("multiple_answers:"):
                                sheet1.write(i, j, "Ответов нет")
                            else:
                                sheet1.write(i, j, ii[2])
                        else:
                            sheet1.write(i, j, "Ответа нет")
                j = j + 1
        i = i + 1
            
    excel_book = os.path.join(".","excel",str(call.data)+".xls")
    book.save(excel_book)
    await asyncio.sleep(3)
    await call.message.reply_document(open(excel_book, 'rb'))
    await asyncio.sleep(3)
    os.remove(excel_book)
    await state.finish()
    await interface_all_begin2(call, state)




def register_get_test_result(dp: Dispatcher):
    dp.register_callback_query_handler(get_test_result, lambda c: c.data == "get_test_result", state=None)
    dp.register_callback_query_handler(get_test_result2, state=get_test.Q1)