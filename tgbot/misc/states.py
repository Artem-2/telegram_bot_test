from aiogram.dispatcher.filters.state import State, StatesGroup



class all(StatesGroup):
#���������
    interface_all_stateBegin = State()
    interface_all_stateQ1 = State()
#����������� �������������
    registration_teachers_statusQ1 = State()
    registration_teachers_statusQ2 = State()
#����������� �������������
    reg_usQ1 = State()
    reg_usQ2 = State()
#�������� ����� ������������
    rename_stateQ1 = State()
    rename_stateQ2 = State()
    rename_stateQ3 = State()
#�������� �����
    test_readQ1 = State()
#����� ����������� �����
    get_testQ1 = State()
#���������� �������� � ����
    test_picturesQ1 = State()
#�������� �������� �� ����
    test_pictures_delQ1 = State()
#�������� �����
    test_del_stateQ1 = State()
    test_del_stateQ2 = State()
#��������� � ����������� �����
    test_activateQ1 = State()
    test_activateQ2 = State()
#��������� ����������� �� ������ 1 ���
    register_get_test_result_one_dayQ1 = State()




#��� ����������� �����
class test_status(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()