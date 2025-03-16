from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from utils.roles import is_admin
from aiogram.fsm.context import FSMContext
from states.states import OrderRegistration
from aiogram import F
from utils.config import admin_username

router = Router()

@router.message(F.text == 'Показать информацию по водителям')
async def show_admin_menu(message: Message):
    if is_admin(message.from_user.id) or message.from_user.username == admin_username:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Информация по водителям", callback_data="show_drivers_info")],
                [InlineKeyboardButton(text="История поездок", callback_data="show_trip_history")],
                [InlineKeyboardButton(text="Статистика", callback_data="show_statistics")],
                [InlineKeyboardButton(text="Зарегистрировать машину", callback_data="register_car")],
                [InlineKeyboardButton(text="Зарегистрировать пользователя", callback_data="register_user")]
            ]
        )
        await message.answer("Меню администратора:", reply_markup=keyboard)
    else:
        await message.answer("Эта команда доступна только администраторам.")

@router.callback_query(lambda c: c.data == "show_drivers_info")
async def show_stats_callback(callback: CallbackQuery):
    stats = "Свободные водители: ...\nЗанятые водители: ..."
    await callback.message.edit_text(stats, reply_markup=get_back_keyboard())
    await callback.answer()

@router.callback_query(lambda c: c.data == "show_trip_history")
async def show_history_callback(callback: CallbackQuery):
    await callback.message.edit_text("История маршрутов на карте.", reply_markup=get_back_keyboard())
    await callback.answer()

@router.callback_query(lambda c: c.data == "show_statistics")
async def show_state_callback(callback: CallbackQuery):
    await callback.message.edit_text("Выберите водителя, статистику которого желаете увидеть", reply_markup=get_back_keyboard())
    stats = "Водители: ..."
    await callback.message.answer(stats)
    await callback.answer()

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
async def back_to_admin_menu(callback: CallbackQuery):
    await show_admin_menu(callback.message)
    await callback.answer()

def get_back_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="back_to_admin_menu")]
        ]
    )