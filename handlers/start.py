from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from utils.roles import is_admin, is_driver
from utils.config import admin_username
from states.states import OrderRegistration

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    # Очищаем состояние
    await state.clear()

    # Определяем роль пользователя
    user_id = message.from_user.id

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
        await message.answer("Добро пожаловать в панель администратора!", reply_markup=keyboard)

    elif is_driver(user_id):
        # Клавиатура для водителя
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Отправить текущий статус", callback_data="send_status")],
                [InlineKeyboardButton(text="Открыть смену", callback_data="open_shift")],
                [InlineKeyboardButton(text="Закрыть смену", callback_data="close_shift")]
            ]
        )
        await message.answer("Добро пожаловать, водитель!", reply_markup=keyboard)

    else:
        # Клавиатура для нового пользователя
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Регистрация", callback_data="register")]
            ]
        )
        await message.answer("Добро пожаловать! Для начала работы необходимо зарегистрироваться.",
                             reply_markup=keyboard)


# Обработчики для callback-запросов
@router.callback_query(lambda c: c.data == "send_status")
async def process_send_status(callback: CallbackQuery):
    from handlers.driver import statuses
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=status, callback_data=f"status_{status}")]
            for status in statuses
        ]
    )
    await callback.message.edit_text("Выберите ваш текущий статус:", reply_markup=keyboard)
    await callback.answer()


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