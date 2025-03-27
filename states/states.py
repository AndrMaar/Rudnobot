from aiogram.fsm.state import StatesGroup, State

class OrderMenu(StatesGroup):
    start_menu = State()
    profile_menu = State()

class OrderRegistration(StatesGroup):

    wait_login = State()
    wait_password = State()

    wait_car_number = State()
    wait_max_weight = State()
    wait_mark = State()
    wait_model = State()

    wait_n = State()

    wait_choise = State()

    wait_bd_continue = State()
    wait_bd_close_continue = State()

    wait_delete_user = State()
    wait_delete_car = State()

class Statuses(StatesGroup):
    wait_driver = State()
    wait_car = State()




