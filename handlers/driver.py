from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from db.database import save_status, binding, binding_end
from aiogram import F
from utils.roles import is_driver
from utils.config import admin_username
from states.states import OrderRegistration

router = Router()

statuses = ["Погрузка", "Разгрузка", "Обед", "Пересменка", "Заправка", "Ремонт", "Свободен"]

@router.message(F.text == "Отправить текущий статус")
async def cmd_status(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=status, callback_data=f"status_{status}")]
            for status in statuses
        ]
    )
    await message.answer("Выберите ваш текущий статус:", reply_markup=keyboard)

@router.callback_query(lambda c: c.data.startswith("status_"))
async def handle_status_callback(callback: CallbackQuery):
    selected_status = callback.data.split("_")[1]
    save_status(user_id=callback.from_user.id, status=selected_status)
    await callback.message.edit_text(f"Ваш статус был обновлен: {selected_status}")
    await callback.answer()

@router.message(F.text == 'Открыть смену')
async def open_bd(message: Message, state: FSMContext):
    if is_driver(message.from_user.id) or message.from_user.username == admin_username:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Отмена", callback_data="cancel_open_shift")]
            ]
        )
        await message.answer("Отправьте номер машины", reply_markup=keyboard)
        await state.set_state(OrderRegistration.wait_bd_continue)
    else:
        await message.answer("Эта команда доступна только водителям.")

@router.callback_query(lambda c: c.data == "cancel_open_shift")
async def cancel_open_shift(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Открытие смены отменено")
    await state.clear()
    await callback.answer()

@router.message(OrderRegistration.wait_bd_continue)
async def open_bd_continue(message: Message, state: FSMContext):
    try:
        binding(telegram_id=message.from_user.id, car_number=message.text)
        await message.answer("Готово")
        await state.clear()
    except Exception as e:
        await message.answer(f"Что-то пошло не так, начните заново. Ошибка: {e}")
        await state.clear()

@router.message(F.text == 'Закрыть смену')
async def close_bd(message: Message, state: FSMContext):
    if is_driver(message.from_user.id) or message.from_user.username == admin_username:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Подтвердить", callback_data="confirm_close_shift"),
                    InlineKeyboardButton(text="Отмена", callback_data="cancel_close_shift")
                ]
            ]
        )
        await message.answer("Вы уверены, что хотите закрыть смену?", reply_markup=keyboard)
    else:
        await message.answer("Эта команда доступна только водителям.")

@router.callback_query(lambda c: c.data == "confirm_close_shift")
async def confirm_close_shift(callback: CallbackQuery, state: FSMContext):
    try:
        binding_end(telegram_id=callback.from_user.id)
        await callback.message.edit_text("Смена успешно закрыта")
        await state.clear()
    except Exception as e:
        await callback.message.edit_text(f"Что-то пошло не так, начните заново. Ошибка: {e}")
        await state.clear()
    await callback.answer()

@router.callback_query(lambda c: c.data == "cancel_close_shift")
async def cancel_close_shift(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Закрытие смены отменено")
    await state.clear()
    await callback.answer()