from aiogram.dispatcher.filters.state import State, StatesGroup



class all(StatesGroup):
#интерфейс
    interface_all_stateBegin = State()
    interface_all_stateQ1 = State()
#создание теста
    test_readQ1 = State()
#вывод результатов теста
    get_testQ1 = State()
#добавление картинки в базу
    test_picturesQ1 = State()
#удаление картинки из базы
    test_pictures_delQ1 = State()
#удаление теста
    test_del_stateQ1 = State()
    test_del_stateQ2 = State()
#активация и деактивация теста
    test_activateQ1 = State()
    test_activateQ2 = State()
#получение результатов не старше 1 дня
    register_get_test_result_one_dayQ1 = State()



#изменеие имени пользователя
class rename_state(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    
#регистрация преподавателя
class registration_teachers_status(StatesGroup):
    Q1 = State()
    Q2 = State()

#регистрация пользователей
class reg_us(StatesGroup):
    Q1 = State()
    Q2 = State()

#для прохождения теста
class test_status(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()