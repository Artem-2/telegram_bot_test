from aiogram.dispatcher.filters.state import State, StatesGroup



class all(StatesGroup):
#интерфейс
    interface_all_stateBegin = State()
    interface_all_stateQ2 = State()
    interface_all_stateQ3 = State()
    interface_all_stateQ4 = State()
#регистрация преподавателя
    registration_teachers_statusQ1 = State()
    registration_teachers_statusQ2 = State()
#регистрация пользователей
    reg_usQ1 = State()
    reg_usQ2 = State()
#изменеие имени пользователя
    rename_stateQ1 = State()
    rename_stateQ2 = State()
    rename_stateQ3 = State()
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




#для прохождения теста
class test_status(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()