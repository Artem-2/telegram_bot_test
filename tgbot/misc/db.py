import sqlite3 
from tgbot.misc.db_create import db_create
#доделать создание преподавателя admina

semaphore = 0

def semaphore_begin():
    global semaphore
    if semaphore == 0:
        semaphore = semaphore + 1
    else:
        s = semaphore
        min = 0
        while s != min:
            if semaphore - s < 0:
                min = min + ((-1)*(semaphore - s))

def semaphore_end():
    global semaphore
    semaphore = semaphore - 1

class BotDB:

    def __init__(self, db_file):
        #подключение к базе данных
        self.conn = sqlite3.connect(db_file)
        self.conn.execute("PRAGMA foreign_keys = 1")
        self.cursor = self.conn.cursor()
        table_array = ["pictures","question_result","teachers","test","test_answer","test_question","test_result","users"]
        flag = 0
        for t in table_array:
            result = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='" + t + "';")
            if result.fetchone()==None :
                flag = 1
        if flag == 1:
            db_create(self)
#######################################################################
    def user_exists(self, user_id):
        semaphore_begin()
        #проверка регистрации пользователя
        result = self.cursor.execute("SELECT id FROM users WHERE user_id = ?",(user_id,))
        r = result.fetchone()
        semaphore_end()
        return r

    def get_user(self, id):
        semaphore_begin()
        #вывод информации о пользователе по id
        result = self.cursor.execute("SELECT user_name, user_group FROM users WHERE id = ?",(id,))
        r = result.fetchone()
        semaphore_end()
        return r

    def user_add(self, user_id , user_name , user_group):
        semaphore_begin()
        #добавление нового пользователя
        self.cursor.execute("INSERT INTO 'users' ('user_id','user_name','user_group') VALUES (?, ?, ?)",(user_id,user_name,user_group))
        self.conn.commit()
        r = self.cursor.lastrowid
        semaphore_end()
        return r

    def get_test_user_rename_number_of_changes(self, user_id):
        semaphore_begin()
        #вывод информации о пользователе по id
        result = self.cursor.execute("SELECT number_of_changes FROM users WHERE user_id = ?",(user_id,))
        r = result.fetchone()
        semaphore_end()
        return r

    def test_user_rename(self, user_name, user_group, number_of_changes, user_id):
        semaphore_begin()
        #изменить имя пользователя
        self.cursor.execute("UPDATE users SET user_name=?, user_group=?, number_of_changes=? WHERE user_id=?",(user_name,user_group, number_of_changes,user_id))
        self.conn.commit()
        r = self.cursor.lastrowid
        semaphore_end()
        return r
#########################################################################
    def get_test_title_attempts_random_mode_questions(self, id):
        semaphore_begin()
        #получить критерии оценок
        result = self.cursor.execute("SELECT title, number_attempts, random_mode, number_questions FROM test WHERE id = ?",(id,))
        r = result.fetchone()
        semaphore_end()
        return r
    

    def get_test_active_mode(self, id):
        semaphore_begin()
        #получить критерии оценок
        result = self.cursor.execute("SELECT active_mode FROM test WHERE id = ?",(id,))
        r = result.fetchone()
        semaphore_end()
        return r

    def test_update_active_mode(self, test_code, active_mode):
        semaphore_begin()
        #активировать деактивировать тест
        self.cursor.execute("UPDATE test SET active_mode=? WHERE test_code=?",(active_mode, test_code))
        self.conn.commit()
        r = self.cursor.lastrowid
        semaphore_end()
        return r

    def get_test_mark(self, id):
        semaphore_begin()
        #получить критерии оценок
        result = self.cursor.execute("SELECT mark_3,mark_4,mark_5 FROM test WHERE id = ?",(id,))
        r = result.fetchone()
        semaphore_end()
        return r

    def get_test_title_code_test(self, user_create_id, active_mode):
        semaphore_begin()
        #получить название и код теста
        result = self.cursor.execute("SELECT title,test_code FROM test WHERE (user_create_id = ? AND active_mode = ?)",(user_create_id,active_mode))
        r = result.fetchall()
        semaphore_end()
        return r

    def get_test_title_test_code_no_active_mode(self, user_create_id):
        semaphore_begin()
        #получить название и код теста
        result = self.cursor.execute("SELECT title,test_code FROM test WHERE user_create_id = ? ",(user_create_id,))
        r = result.fetchall()
        semaphore_end()
        return r

    def get_test_title_test_code_no_active_mode_admin(self):
        semaphore_begin()
        #получить название и код теста
        result = self.cursor.execute("SELECT title,test_code,user_create_id FROM test",())
        r = result.fetchall()
        semaphore_end()
        return r

    def test_del(self, id):
        semaphore_begin()
        #удалить тест
        self.cursor.execute("DELETE FROM test WHERE id = ?",(id,))
        self.conn.commit()
        r = self.cursor.lastrowid
        semaphore_end()
        return r

    def get_test(self, test_code):
        semaphore_begin()
        #получить id теста
        result = self.cursor.execute("SELECT id, time_question FROM test WHERE test_code = ?",(test_code,))
        r = result.fetchone()
        semaphore_end()
        return r

    def get_test_user_create_id(self, user_create_id, test_code):
        semaphore_begin()
        #получить id теста
        result = self.cursor.execute("SELECT id FROM test WHERE (user_create_id = ? AND test_code = ?)",(user_create_id, test_code))
        r = result.fetchall()
        semaphore_end()
        return r

    def test_add(self, user_create_id , title, test_code, time_question, random_mode, number_attempts, number_questions, mark_3, mark_4, mark_5):
        semaphore_begin()
        #добавление нового теста без вопросов
        self.cursor.execute("INSERT INTO 'test' ('user_create_id', 'title','test_code','time_question','random_mode','number_attempts','number_questions','mark_3','mark_4','mark_5') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(user_create_id,title,test_code,time_question, random_mode, number_attempts, number_questions, mark_3, mark_4, mark_5))
        self.conn.commit()
        r = self.cursor.lastrowid
        semaphore_end()
        return r
#########################################################################
    def get_question_test(self, fk_id):
        semaphore_begin()
        #получить id time_question теста
        result = self.cursor.execute("SELECT id, question, time FROM test_question WHERE fk_id = ?",(fk_id,))
        r = result.fetchall()
        semaphore_end()
        return r

    def get_question_test_pictures_id(self, id):
        semaphore_begin()
        #получить код картинки
        result = self.cursor.execute("SELECT pictures_id FROM test_question WHERE id = ?",(id,))
        r = result.fetchone()
        semaphore_end()
        return r

    def question_test_add(self, fk_id , question):
        semaphore_begin()
        #добавление вопроса в тест
        self.cursor.execute("INSERT INTO 'test_question' ('fk_id','question') VALUES (?, ?)",(fk_id,question))
        self.conn.commit()
        r = self.cursor.lastrowid
        semaphore_end()
        return r
    
    def question_test_add_pictures(self, pictures_id, id):
        semaphore_begin()
        #добавление картинки к вопросу
        self.cursor.execute("UPDATE test_question SET pictures_id=? WHERE id=?",(pictures_id,id))
        self.conn.commit()
        r = self.cursor.lastrowid
        semaphore_end()
        return r
##########################################################################
    def get_answer_test(self, fk_id):
        semaphore_begin()
        #получить idtime_question теста
        result = self.cursor.execute("SELECT answer, right_answer, id FROM test_answer WHERE fk_id = ?",(fk_id,))
        r = result.fetchall()
        semaphore_end()
        return r

    def get_answer_test_right_v2(self, fk_id):
        semaphore_begin()
        #получить количество правильных ответов
        result = self.cursor.execute("SELECT id FROM test_answer WHERE (fk_id = ? AND right_answer = 1)",(fk_id,))
        r = result.fetchall()
        semaphore_end()
        return r

    def get_answer_test_answer(self, id):
        semaphore_begin()
        #получить idtime_question теста
        result = self.cursor.execute("SELECT answer FROM test_answer WHERE id = ?",(id,))
        r = result.fetchone()
        semaphore_end()
        return r

    def answer_test_add(self, fk_id , answer, right_answer):
        semaphore_begin()
        #добавление ответа к вопросу
        self.cursor.execute("INSERT INTO 'test_answer' ('fk_id','answer','right_answer') VALUES (?, ?, ?)",(fk_id,answer,right_answer))
        self.conn.commit()
        r = self.cursor.lastrowid
        semaphore_end()
        return r

    def answer_test_add_time(self, id, time):
        semaphore_begin()
        #добавление результата к прохождению
        self.cursor.execute("UPDATE test_question SET time=? WHERE id=?",(time,id))
        self.conn.commit()
        r = self.cursor.lastrowid
        semaphore_end()
        return r
###########################################################################
    def test_result_del(self, id):
        semaphore_begin()
        #удалить результаты теста
        self.cursor.execute("DELETE FROM test_result WHERE id = ?",(id,))
        self.conn.commit()
        r = self.cursor.lastrowid
        semaphore_end()
        return r

    def get_test_result_all(self, test_id):
        semaphore_begin()
        #получить id теста который проходит пользователь
        result = self.cursor.execute("SELECT user_id, result, mark, data, id FROM test_result WHERE test_id = ?",(test_id,))
        r = result.fetchall()
        semaphore_end()
        return r

    def get_test_result(self, user_id , test_id):
        semaphore_begin()
        #получить id теста который проходит пользователь
        result = self.cursor.execute("SELECT id FROM test_result WHERE (user_id = ? AND test_id = ?)",(user_id,test_id))
        r = result.fetchall()
        semaphore_end()
        return r

    def test_result_add(self, user_id , test_id):
        semaphore_begin()
        #добавление прохождения теста
        self.cursor.execute("INSERT INTO 'test_result' ('user_id','test_id') VALUES (?, ?)",(user_id,test_id))
        self.conn.commit()
        r = self.cursor.lastrowid
        semaphore_end()
        return r

    def test_result_add_result(self, result, id, mark):
        semaphore_begin()
        #добавление результата к прохождению
        self.cursor.execute("UPDATE test_result SET result=? WHERE id=?",(result,id))
        self.cursor.execute("UPDATE test_result SET mark=? WHERE id=?",(mark,id))
        self.conn.commit()
        r = self.cursor.lastrowid
        semaphore_end()
        return r
###########################################################################
    def get_question_result(self, fk_id):
        semaphore_begin()
        #получить idtime_question теста
        result = self.cursor.execute("SELECT result_question FROM question_result WHERE fk_id = ?",(fk_id,))
        r = result.fetchall()
        semaphore_end()
        return r

    def get_question_result_id_question_id_answer_text_response(self, fk_id):
        semaphore_begin()
        #получить idtime_question теста
        result = self.cursor.execute("SELECT id_question,id_answer,text_response FROM question_result WHERE fk_id = ?",(fk_id,))
        r = result.fetchall()
        semaphore_end()
        return r

    def answer_question_result(self, fk_id, result_question, id_question, id_answer):
        semaphore_begin()
        #добавление ответа к вопросу
        self.cursor.execute("INSERT INTO 'question_result' ('fk_id','result_question','id_question','id_answer') VALUES (?, ?, ?, ?)",(fk_id,result_question,id_question, id_answer))
        self.conn.commit()
        r = self.cursor.lastrowid
        semaphore_end()
        return r

    def answer_question_result_update(self, id, fk_id, result_question, id_question, id_answer):
        semaphore_begin()
        #добавление ответа к вопросу
        self.cursor.execute("UPDATE question_result SET fk_id = ?, result_question = ?, id_question = ?, id_answer = ? WHERE id=?",(fk_id, result_question, id_question, id_answer, id))
        self.conn.commit()
        r = self.cursor.lastrowid
        semaphore_end()
        return r

    def answer_question_result_multiple_answers(self, fk_id, result_question, id_question, text_response):
        semaphore_begin()
        #добавление ответа к вопросу
        self.cursor.execute("INSERT INTO 'question_result' ('fk_id','result_question','id_question','text_response') VALUES (?, ?, ?, ?)",(fk_id,result_question,id_question, text_response))
        self.conn.commit()
        r = self.cursor.lastrowid
        semaphore_end()
        return r

    def answer_question_result_multiple_answers_update(self, id, fk_id, result_question, id_question, text_response):
        semaphore_begin()
        #добавление ответа к вопросу
        self.cursor.execute("UPDATE question_result SET fk_id = ?, result_question = ?, id_question = ?, text_response = ? WHERE id=?",(fk_id, result_question, id_question, text_response, id))
        self.conn.commit()
        r = self.cursor.lastrowid
        semaphore_end()
        return r

    def answer_question_result_text_response_update(self, id, text_response):
        semaphore_begin()
        #добавление ответа к вопросу
        self.cursor.execute("UPDATE question_result SET text_response = ? WHERE id=?",(text_response, id))
        self.conn.commit()
        r = self.cursor.lastrowid
        semaphore_end()
        return r
###########################################################################
    def get_pictures_id(self, pictures_code):
        semaphore_begin()
        #получить id картинки
        result = self.cursor.execute("SELECT id FROM pictures WHERE pictures_code = ?",(pictures_code,))
        r = result.fetchone()
        semaphore_end()
        return r

    def pictures_add(self, pictures_code, user_create_id):
        semaphore_begin()
        #добавление новой картинки
        self.cursor.execute("INSERT INTO 'pictures' ('pictures_code','user_create_id') VALUES (?, ?)",(pictures_code,user_create_id))
        self.conn.commit()
        r = self.cursor.lastrowid
        semaphore_end()
        return r

    def pictures_del(self, pictures_code):
        semaphore_begin()
        #удалить тест
        self.cursor.execute("DELETE FROM pictures WHERE pictures_code = ?",(pictures_code,))
        self.conn.commit()
        r = self.cursor.lastrowid
        semaphore_end()
        return r

    def get_pictures_pictures_code(self, user_create_id):
        semaphore_begin()
        #получить id картинки
        result = self.cursor.execute("SELECT pictures_code FROM pictures WHERE user_create_id = ?",(user_create_id,))
        r = result.fetchall()
        semaphore_end()
        return r
###########################################################################
    def get_teachers_name(self, user_id):
        semaphore_begin()
        #получить 
        result = self.cursor.execute("SELECT name FROM teachers WHERE user_id = ?",(user_id,))
        r = result.fetchone()
        semaphore_end()
        return r

    def get_teachers_password(self, password_registration):
        semaphore_begin()
        #получить 
        result = self.cursor.execute("SELECT id FROM teachers WHERE password_registration = ?",(password_registration,))
        r = result.fetchone()
        semaphore_end()
        return r

    def teachers_password_add(self, password_registration, date_creative_password, user_id):
        semaphore_begin()
        #добавление результата к прохождению
        self.cursor.execute("UPDATE teachers SET password_registration=?, date_creative_password=? WHERE user_id=?",(password_registration, date_creative_password,user_id))
        self.conn.commit()
        r = self.cursor.lastrowid
        semaphore_end()
        return r

    def teachers_add(self, name, user_id, referral):
        semaphore_begin()
        #добавление новой картинки
        self.cursor.execute("INSERT INTO 'teachers' ('name','user_id','referral') VALUES (?, ?, ?)",(name, user_id, referral))
        self.conn.commit()
        r = self.cursor.lastrowid
        semaphore_end()
        return r

    def get_teachers_data(self, id):
        semaphore_begin()
        #получить 
        result = self.cursor.execute("SELECT date_creative_password FROM teachers WHERE id = ?",(id,))
        r = result.fetchone()
        semaphore_end()
        return r

    def get_teachers_user_id(self, id):
        semaphore_begin()
        #получить 
        result = self.cursor.execute("SELECT user_id FROM teachers WHERE id = ?",(id,))
        r = result.fetchone()
        semaphore_end()
        return r

    def close(self):
        self.conn.close()