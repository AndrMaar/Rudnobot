from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, KeyboardButton, \
    ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from db.database import check_phone, set_user_by_telegram_id, get_user_by_telegram_id
from utils.roles import is_admin, is_driver
from utils.config import admin_username
from states.states import OrderRegistration
import asyncio

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, text):
    # Очищаем состояние
    await state.clear()

    # Определяем роль пользователя
    user_id = message.chat.id

    # Создаем клавиатуру в зависимости от роли
    if is_admin(user_id) or message.from_user.username == admin_username:
        # Клавиатура для администратора
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Информация по водителям", callback_data="show_drivers_info")],
                [InlineKeyboardButton(text="История поездок", callback_data="show_trip_history")],
                [InlineKeyboardButton(text="Статистика", callback_data="show_statistics")],
                [InlineKeyboardButton(text="Зарегистрировать машину", callback_data="register_car")],
                [InlineKeyboardButton(text="Зарегистрировать пользователя", callback_data="register_user")]
            ]
        )
        sent_message = await message.answer("Добро пожаловать в панель администратора!", reply_markup=keyboard)

        # Сохраняем ID сообщения
        data = await state.get_data()
        message_ids = data.get("message_ids", [])
        message_ids.append(sent_message.message_id)
        await state.update_data(message_ids=message_ids)

    elif is_driver(user_id):
        # Клавиатура для водителя
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Отправить текущий статус", callback_data="send_status")],
                [InlineKeyboardButton(text="Открыть смену", callback_data="open_shift")],
                [InlineKeyboardButton(text="Закрыть смену", callback_data="close_shift")]
            ]
        )
        sent_message = await message.answer("Добро пожаловать, водитель!", reply_markup=keyboard)

        # Сохраняем ID сообщения
        data = await state.get_data()
        message_ids = data.get("message_ids", [])
        message_ids.append(sent_message.message_id)
        await state.update_data(message_ids=message_ids)

    else:
        kb_list = [[KeyboardButton(text="Отправить номер телефона", request_contact=True)]]
        sent_message = await message.answer('Вам необходимо войти',
                                            reply_markup=ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True,
                                                                             one_time_keyboard=True))

        # Сохраняем ID сообщения
        data = await state.get_data()
        message_ids = data.get("message_ids", [])
        message_ids.append(sent_message.message_id)
        await state.update_data(message_ids=message_ids)

        await state.set_state(OrderRegistration.wait_n)





# Обработчики для callback-запросов




@router.callback_query(lambda c: c.data == "open_shift")
async def process_open_shift(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Отправьте номер машины")
    await state.set_state(OrderRegistration.wait_bd_continue)
    await callback.answer()


@router.callback_query(lambda c: c.data == "close_shift")
async def process_close_shift(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Подтвердить", callback_data="confirm_close_shift"),
                InlineKeyboardButton(text="Отмена", callback_data="cancel_close_shift")
            ]
        ]
    )
    await callback.message.edit_text("Вы уверены, что хотите закрыть смену?",
                                     reply_markup=keyboard)
    await callback.answer()


@router.callback_query(lambda c: c.data == "register")
async def process_register(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите ваш логин:")
    await state.set_state(OrderRegistration.wait_login)
    await callback.answer()