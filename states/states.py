from aiogram.fsm.state import StatesGroup, State

class OrderMenu(StatesGroup):
    start_menu = State()
    profile_menu = State()

class OrderRegistration(StatesGroup):
    wait_password = State()
    wait_name = State()
    wait_surname = State()
    wait_lastname = State()
    yn = State()
    password = State()
    wait_car_number = State()
    wait_max_weight = State()
    wait_mark = State()
    wait_model = State()


