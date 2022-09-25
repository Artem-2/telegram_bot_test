from aiogram.dispatcher.filters.state import State, StatesGroup

class interface_all_state(StatesGroup):
    Begin = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()


class registration_teachers_status(StatesGroup):
    Q1 = State()
    Q2 = State()


#для прохождения теста
class test_status(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()

#регистрация пользователей
class reg_us(StatesGroup):
    Q1 = State()
    Q2 = State()

#изменеие имени пользователя
class rename_state(StatesGroup):
    Q1 = State()
    Q2 = State()

#создание теста
class test_read(StatesGroup):
    Q1 = State()

#вывод результатов теста
class get_test(StatesGroup):
    Q1 = State()

#добавление картинки в базу
class test_pictures(StatesGroup):
    Q1 = State()

class test_pictures_del(StatesGroup):
    Q1 = State()

#удаление теста
class test_del_state(StatesGroup):
    Q1 = State()
    Q2 = State()

#активация и деактивация теста
class test_activate(StatesGroup):
    Q1 = State()
    Q2 = State()