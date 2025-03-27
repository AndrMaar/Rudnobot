from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from db.database import remove_user, drivers_list, get_driver_statuses, cars_list, get_car_statuses
from utils.roles import is_admin
from aiogram.fsm.context import FSMContext
from states.states import OrderRegistration, Statuses
from aiogram import F
from utils.config import admin_username
from utils.message_utils import clean_chat_and_restart
import asyncio

router = Router()


@router.message(F.text == 'Показать информацию по водителям')
async def show_admin_menu(message: Message, state: FSMContext):
    if is_admin(message.from_user.id) or message.from_user.username == admin_username:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Зарегистрировать машину", callback_data="register_car")],
                [InlineKeyboardButton(text="Зарегистрировать пользователя", callback_data="register_user")],
                [InlineKeyboardButton(text="Удалить машину", callback_data="delete_car")],
                [InlineKeyboardButton(text="Удалить пользователя", callback_data="delete_user")],
                [InlineKeyboardButton(text="Просмотр статусов", callback_data="status")]
            ]
        )
        sent_message = await message.answer("Меню администратора:", reply_markup=keyboard)

        # Сохраняем ID сообщения
        data = await state.get_data()
        message_ids = data.get("message_ids", [])
        message_ids.append(sent_message.message_id)
        await state.update_data(message_ids=message_ids)

    else:
        sent_message = await message.answer("Эта команда доступна только администраторам.")

        # Сохраняем ID сообщения
        data = await state.get_data()
        message_ids = data.get("message_ids", [])
        message_ids.append(sent_message.message_id)
        await state.update_data(message_ids=message_ids)


@router.callback_query(lambda c: c.data == "register_car")
async def reg_car_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Отправьте номер машины")
    await state.set_state(OrderRegistration.wait_car_number)
    await callback.answer()


@router.callback_query(lambda c: c.data == "register_user")
async def reg_user_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Отправьте логин")
    await state.set_state(OrderRegistration.wait_login)
    await callback.answer()


@router.callback_query(lambda c: c.data == "back_to_admin_menu")
async def back_to_admin_menu(callback: CallbackQuery, state: FSMContext):
    await clean_chat_and_restart(callback.message, state)
    await callback.answer()


@router.callback_query(lambda c: c.data == "delete_user")
async def delete_user(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Отправьте телефон того пользователя, которого хотите удалить")
    await state.set_state(OrderRegistration.wait_delete_user)
    await callback.answer()




@router.callback_query(lambda c: c.data == "delete_car")
async def delete_car(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Отправьте номер той машины, которую хотите удалить")
    await state.set_state(OrderRegistration.wait_delete_car)
    await callback.answer()

@router.callback_query(lambda c: c.data == "status")
async def choose_status(callback: CallbackQuery, state: FSMContext):

    await callback.message.edit_text("Чей статус вы хотите просмотреть?")
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Водителя", callback_data="driver_status")],
            [InlineKeyboardButton(text="Автомобиля", callback_data="car_status")]
        ]
    )
    await callback.message.edit_text("Чей статус вы хотите просмотреть?", reply_markup=keyboard)

@router.callback_query(lambda c: c.data == "driver_status")
async def choose_driver(callback: CallbackQuery, state: FSMContext):
    drivers = drivers_list()
    keyboard = []
    for driver in drivers:
        keyboard.append([KeyboardButton(text=driver[0])])
    await callback.message.answer("Выберите водителя на смене", reply_markup=ReplyKeyboardMarkup(keyboard=keyboard), one_time_keyboard=True)
    await state.set_state(Statuses.wait_driver)

@router.callback_query(lambda c: c.data == "car_status")
async def choose_driver(callback: CallbackQuery, state: FSMContext):
    cars = cars_list()
    keyboard = []
    for car in cars:
        print(car)
        keyboard.append([KeyboardButton(text=car[0])])
    await callback.message.answer("Выберите автомобиль на смене", reply_markup=ReplyKeyboardMarkup(keyboard=keyboard),
                                  one_time_keyboard=True)
    await state.set_state(Statuses.wait_car)

@router.message(Statuses.wait_car)
async def driver_statuses(message: Message, state: FSMContext):
    car_number = message.text
    statuses = get_car_statuses(car_number)
    message_text = f"Cтатус автомобиля {car_number}:"
    for status in statuses:
        message_text += f"\n- Время: {status[1]}: Статус: {status[0]}"
    await message.answer(message_text)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Зарегистрировать машину", callback_data="register_car")],
            [InlineKeyboardButton(text="Зарегистрировать пользователя", callback_data="register_user")],
            [InlineKeyboardButton(text="Удалить машину", callback_data="delete_car")],
            [InlineKeyboardButton(text="Удалить пользователя", callback_data="delete_user")],
            [InlineKeyboardButton(text="Просмотр статусов", callback_data="status")]
        ]
    )
    await message.answer("Меню администратора:", reply_markup=keyboard)
    await state.clear()

@router.message(Statuses.wait_driver)
async def driver_statuses(message: Message, state: FSMContext):
    driver_name = message.text
    statuses = get_driver_statuses(driver_name)
    message_text = f"Статус водителя {driver_name}:"
    for status in statuses:
        message_text += f"\n- Время: {status[1]}: Статус: {status[0]}"
    await message.answer(message_text)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Зарегистрировать машину", callback_data="register_car")],
            [InlineKeyboardButton(text="Зарегистрировать пользователя", callback_data="register_user")],
            [InlineKeyboardButton(text="Удалить машину", callback_data="delete_car")],
            [InlineKeyboardButton(text="Удалить пользователя", callback_data="delete_user")],
            [InlineKeyboardButton(text="Просмотр статусов", callback_data="status")]
        ]
    )
    await message.answer("Меню администратора:", reply_markup=keyboard)
    await state.clear()

def get_back_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="back_to_admin_menu")]
        ]
    )