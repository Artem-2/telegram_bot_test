from aiogram.dispatcher.filters.state import State, StatesGroup

class interface_all_state(StatesGroup):
    Begin = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()


class registration_teachers_status(StatesGroup):
    Q1 = State()
    Q2 = State()


#��� ����������� �����
class test_status(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()

#����������� �������������
class reg_us(StatesGroup):
    Q1 = State()
    Q2 = State()

#�������� ����� ������������
class rename_state(StatesGroup):
    Q1 = State()
    Q2 = State()

#�������� �����
class test_read(StatesGroup):
    Q1 = State()

#����� ����������� �����
class get_test(StatesGroup):
    Q1 = State()

#���������� �������� � ����
class test_pictures(StatesGroup):
    Q1 = State()

class test_pictures_del(StatesGroup):
    Q1 = State()

#�������� �����
class test_del_state(StatesGroup):
    Q1 = State()
    Q2 = State()

#��������� � ����������� �����
class test_activate(StatesGroup):
    Q1 = State()
    Q2 = State()