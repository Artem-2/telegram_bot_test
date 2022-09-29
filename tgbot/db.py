import sqlite3 




class BotDB:

    def __init__(self, db_file):
        #подключение к базе данных
        self.conn = sqlite3.connect(db_file)
        self.conn.execute("PRAGMA foreign_keys = 1")
        self.cursor = self.conn.cursor()
#######################################################################
    def user_exists(self, user_id):
        #проверка регистрации пользователя
        result = self.cursor.execute("SELECT id FROM users WHERE user_id = ?",(user_id,))
        return result.fetchone()

    def get_user(self, id):
        #вывод информации о пользователе по id
        result = self.cursor.execute("SELECT user_name, user_group FROM users WHERE id = ?",(id,))
        return result.fetchone()

    def user_add(self, user_id , user_name , user_group):
        #добавление нового пользователя
        self.cursor.execute("INSERT INTO 'users' ('user_id','user_name','user_group') VALUES (?, ?, ?)",(user_id,user_name,user_group))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_test_user_rename_number_of_changes(self, user_id):
        #вывод информации о пользователе по id
        result = self.cursor.execute("SELECT number_of_changes FROM users WHERE user_id = ?",(user_id,))
        return result.fetchone()

    def test_user_rename(self, user_name, user_group, number_of_changes, user_id):
        #изменить имя пользователя
        self.cursor.execute("UPDATE users SET user_name=?, user_group=?, number_of_changes=? WHERE user_id=?",(user_name,user_group, number_of_changes,user_id))
        self.conn.commit()
        return self.cursor.lastrowid
#########################################################################
    def get_test_active_mode(self, id):
        #получить критерии оценок
        result = self.cursor.execute("SELECT active_mode FROM test WHERE id = ?",(id,))
        return result.fetchone()

    def test_update_active_mode(self, test_code, active_mode):
        #активировать деактивировать тест
        self.cursor.execute("UPDATE test SET active_mode=? WHERE test_code=?",(active_mode, test_code))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_test_mark(self, id):
        #получить критерии оценок
        result = self.cursor.execute("SELECT mark_3,mark_4,mark_5 FROM test WHERE id = ?",(id,))
        return result.fetchone()

    def get_test_title_code_test(self, user_create_id, active_mode):
        #получить название и код теста
        result = self.cursor.execute("SELECT title,test_code FROM test WHERE (user_create_id = ? AND active_mode = ?)",(user_create_id,active_mode))
        return result.fetchall()

    def get_test_title_test_code_no_active_mode(self, user_create_id):
        #получить название и код теста
        result = self.cursor.execute("SELECT title,test_code FROM test WHERE user_create_id = ? ",(user_create_id,))
        return result.fetchall()

    def get_test_title(self, id):
        #получить критерии оценок
        result = self.cursor.execute("SELECT title FROM test WHERE id = ?",(id,))
        return result.fetchone()

    def get_test_attempts(self, id):
        #получить колличество попыток
        result = self.cursor.execute("SELECT number_attempts FROM test WHERE id = ?",(id,))
        return result.fetchone()

    def get_test_questions(self, id):
        #получить колличество вопросов
        result = self.cursor.execute("SELECT number_questions FROM test WHERE id = ?",(id,))
        return result.fetchone()

    def get_test_random_mode(self, id):
        #получить колличество вопросов
        result = self.cursor.execute("SELECT random_mode FROM test WHERE id = ?",(id,))
        return result.fetchone()

    def test_del(self, id):
        #удалить тест
        self.cursor.execute("DELETE FROM test WHERE id = ?",(id,))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_test(self, test_code):
        #получить id теста
        result = self.cursor.execute("SELECT id, time_question FROM test WHERE test_code = ?",(test_code,))
        return result.fetchone()

    def get_test_user_create_id(self, user_create_id, test_code):
        #получить id теста
        result = self.cursor.execute("SELECT id FROM test WHERE (user_create_id = ? AND test_code = ?)",(user_create_id, test_code))
        return result.fetchall()

    def test_add(self, user_create_id , title, test_code, time_question, random_mode, number_attempts, number_questions, mark_3, mark_4, mark_5):
        #добавление нового теста без вопросов
        self.cursor.execute("INSERT INTO 'test' ('user_create_id', 'title','test_code','time_question','random_mode','number_attempts','number_questions','mark_3','mark_4','mark_5') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(user_create_id,title,test_code,time_question, random_mode, number_attempts, number_questions, mark_3, mark_4, mark_5))
        self.conn.commit()
        return self.cursor.lastrowid
#########################################################################
    def get_question_test(self, fk_id):
        #получить id time_question теста
        result = self.cursor.execute("SELECT id, question, time FROM test_question WHERE fk_id = ?",(fk_id,))
        return result.fetchall()

    def get_question_test_pictures_id(self, id):
        #получить код картинки
        result = self.cursor.execute("SELECT pictures_id FROM test_question WHERE id = ?",(id,))
        return result.fetchone()

    def question_test_add(self, fk_id , question):
        #добавление вопроса в тест
        self.cursor.execute("INSERT INTO 'test_question' ('fk_id','question') VALUES (?, ?)",(fk_id,question))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def question_test_add_pictures(self, pictures_id, id):
        #добавление картинки к вопросу
        self.cursor.execute("UPDATE test_question SET pictures_id=? WHERE id=?",(pictures_id,id))
        self.conn.commit()
        return self.cursor.lastrowid
##########################################################################
    def get_answer_test(self, fk_id):
        #получить idtime_question теста
        result = self.cursor.execute("SELECT answer, right_answer, id FROM test_answer WHERE fk_id = ?",(fk_id,))
        return result.fetchall()

    def get_answer_test_right(self, fk_id):
        #получить количество правильных ответов
        result = self.cursor.execute("SELECT answer id FROM test_answer WHERE (fk_id = ? AND right_answer = 1)",(fk_id,))
        return result.fetchall()

    def get_answer_test_answer(self, id):
        #получить idtime_question теста
        result = self.cursor.execute("SELECT answer FROM test_answer WHERE id = ?",(id,))
        return result.fetchone()

    def answer_test_add(self, fk_id , answer, right_answer):
        #добавление ответа к вопросу
        self.cursor.execute("INSERT INTO 'test_answer' ('fk_id','answer','right_answer') VALUES (?, ?, ?)",(fk_id,answer,right_answer))
        self.conn.commit()
        return self.cursor.lastrowid

    def answer_test_add_time(self, id, time):
        #добавление результата к прохождению
        self.cursor.execute("UPDATE test_question SET time=? WHERE id=?",(time,id))
        self.conn.commit()
        return self.cursor.lastrowid
###########################################################################
    def get_test_result_all(self, test_id):
        #получить id теста который проходит пользователь
        result = self.cursor.execute("SELECT user_id, result, mark, data, id FROM test_result WHERE test_id = ?",(test_id,))
        return result.fetchall()

    def get_test_result(self, user_id , test_id):
        #получить id теста который проходит пользователь
        result = self.cursor.execute("SELECT id FROM test_result WHERE (user_id = ? AND test_id = ?)",(user_id,test_id))
        return result.fetchall()

    def test_result_add(self, user_id , test_id):
        #добавление прохождения теста
        self.cursor.execute("INSERT INTO 'test_result' ('user_id','test_id') VALUES (?, ?)",(user_id,test_id))
        self.conn.commit()
        return self.cursor.lastrowid

    def test_result_add_result(self, result, id, mark):
        #добавление результата к прохождению
        self.cursor.execute("UPDATE test_result SET result=? WHERE id=?",(result,id))
        self.cursor.execute("UPDATE test_result SET mark=? WHERE id=?",(mark,id))
        self.conn.commit()
        return self.cursor.lastrowid
###########################################################################
    def get_question_result(self, fk_id):
        #получить idtime_question теста
        result = self.cursor.execute("SELECT result_question FROM question_result WHERE fk_id = ?",(fk_id,))
        return result.fetchall()

    
    def get_question_result_id_question_id_answer_text_response(self, fk_id):
        #получить idtime_question теста
        result = self.cursor.execute("SELECT id_question,id_answer,text_response FROM question_result WHERE fk_id = ?",(fk_id,))
        return result.fetchall()

    def answer_question_result(self, fk_id, result_question, id_question, id_answer):
        #добавление ответа к вопросу
        self.cursor.execute("INSERT INTO 'question_result' ('fk_id','result_question','id_question','id_answer') VALUES (?, ?, ?, ?)",(fk_id,result_question,id_question, id_answer))
        self.conn.commit()
        return self.cursor.lastrowid

    def answer_question_result_update(self, id, fk_id, result_question, id_question, id_answer):
        #добавление ответа к вопросу
        self.cursor.execute("UPDATE question_result SET fk_id = ?, result_question = ?, id_question = ?, id_answer = ? WHERE id=?",(fk_id, result_question, id_question, id_answer, id))
        self.conn.commit()
        return self.cursor.lastrowid

    def answer_question_result2(self, fk_id, result_question, id_question):
        #добавление ответа к вопросу
        self.cursor.execute("INSERT INTO 'question_result' ('fk_id','result_question','id_question') VALUES (?, ?, ?)",(fk_id,result_question,id_question))
        self.conn.commit()
        return self.cursor.lastrowid

    def answer_question_result_multiple_answers(self, fk_id, result_question, id_question, text_response):
        #добавление ответа к вопросу
        self.cursor.execute("INSERT INTO 'question_result' ('fk_id','result_question','id_question','text_response') VALUES (?, ?, ?, ?)",(fk_id,result_question,id_question, text_response))
        self.conn.commit()
        return self.cursor.lastrowid

    def answer_question_result_multiple_answers_update(self, id, fk_id, result_question, id_question, text_response):
        #добавление ответа к вопросу
        self.cursor.execute("UPDATE question_result SET fk_id = ?, result_question = ?, id_question = ?, text_response = ? WHERE id=?",(fk_id, result_question, id_question, text_response, id))
        self.conn.commit()
        return self.cursor.lastrowid

    def answer_question_result_text_response(self, fk_id, id_question, text_response):
        #добавление ответа к вопросу
        self.cursor.execute("INSERT INTO 'question_result' ('fk_id','id_question','text_response') VALUES (?, ?, ?)",(fk_id,id_question,text_response))
        self.conn.commit()
        return self.cursor.lastrowid

    def answer_question_result_text_response_update(self, id, text_response):
        #добавление ответа к вопросу
        self.cursor.execute("UPDATE question_result SET text_response = ? WHERE id=?",(text_response, id))
        self.conn.commit()
        return self.cursor.lastrowid
###########################################################################
    def get_pictures_id(self, pictures_code):
        #получить id картинки
        result = self.cursor.execute("SELECT id FROM pictures WHERE pictures_code = ?",(pictures_code,))
        return result.fetchone()

    def pictures_add(self, pictures_code, user_create_id):
        #добавление новой картинки
        self.cursor.execute("INSERT INTO 'pictures' ('pictures_code','user_create_id') VALUES (?, ?)",(pictures_code,user_create_id))
        self.conn.commit()
        return self.cursor.lastrowid

    def pictures_del(self, pictures_code):
        #удалить тест
        self.cursor.execute("DELETE FROM pictures WHERE pictures_code = ?",(pictures_code,))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_pictures_pictures_code(self, user_create_id):
        #получить id картинки
        result = self.cursor.execute("SELECT pictures_code FROM pictures WHERE user_create_id = ?",(user_create_id,))
        return result.fetchall()
###########################################################################
    def get_teachers_name(self, user_id):
        #получить 
        result = self.cursor.execute("SELECT name FROM teachers WHERE user_id = ?",(user_id,))
        return result.fetchone()

    def get_teachers_password(self, password_registration):
        #получить 
        result = self.cursor.execute("SELECT id FROM teachers WHERE password_registration = ?",(password_registration,))
        return result.fetchone()

    def teachers_password_add(self, password_registration, date_creative_password, user_id):
        #добавление результата к прохождению
        self.cursor.execute("UPDATE teachers SET password_registration=?, date_creative_password=? WHERE user_id=?",(password_registration, date_creative_password,user_id))
        self.conn.commit()
        return self.cursor.lastrowid

    def teachers_add(self, name, user_id, referral):
        #добавление новой картинки
        self.cursor.execute("INSERT INTO 'teachers' ('name','user_id','referral') VALUES (?, ?, ?)",(name, user_id, referral))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_teachers_data(self, id):
        #получить 
        result = self.cursor.execute("SELECT date_creative_password FROM teachers WHERE id = ?",(id,))
        return result.fetchone()

    def get_teachers_user_id(self, id):
        #получить 
        result = self.cursor.execute("SELECT user_id FROM teachers WHERE id = ?",(id,))
        return result.fetchone()

    def close(self):
        self.conn.close()