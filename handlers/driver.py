import asyncio

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from db.database import save_status, binding, binding_end, check_shift_status, create_status
from aiogram import F
from utils.roles import is_driver
from utils.config import admin_username
from states.states import OrderRegistration
from utils.message_utils import clean_chat_and_restart

router = Router()

statuses = ["Погрузка", "Разгрузка", "Обед", "Пересменка", "Заправка", "Ремонт", "Свободен"]

@router.message(F.text == "Отправить текущий статус")
async def cmd_status(message: Message):
    if check_shift_status(message.from_user.id):
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=status, callback_data=f"status_{status}")]
                for status in statuses
            ]
        )
        await message.answer("Выберите ваш текущий статус:", reply_markup=keyboard)
    else:
        await message.answer(
            "Для отправки статуса необходимо сначала открыть смену. Используйте команду 'Открыть смену'.")

@router.callback_query(lambda c: c.data.startswith("status_"))
async def handle_status_callback(callback: CallbackQuery,state:FSMContext):
    selected_status = callback.data.split("_")[1]
    save_status(user_id=callback.from_user.id, status=selected_status)
    await callback.message.edit_text(f"Ваш статус был обновлен: {selected_status}")
    await callback.answer()

    await asyncio.sleep(2)

    await clean_chat_and_restart(callback.message, state)

@router.callback_query(lambda c: c.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    await clean_chat_and_restart(callback.message, state)
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


    await asyncio.sleep(1)
    await clean_chat_and_restart(callback.message, state)

    await callback.answer()
@router.message(OrderRegistration.wait_bd_continue)
async def open_bd_continue(message: Message, state: FSMContext):
    try:
        binding(telegram_id=message.from_user.id, car_number=message.text)
        sent_message = await message.answer("Смена успешно открыта")

        # Сохраняем ID сообщения
        data = await state.get_data()
        message_ids = data.get("message_ids", [])
        message_ids.append(sent_message.message_id)
        await state.update_data(message_ids=message_ids)

        await state.clear()

        # Возвращаемся в меню
        await asyncio.sleep(1)
        await clean_chat_and_restart(message, state)
    except Exception as e:
        await message.answer(f"Что-то пошло не так, начните заново. Ошибка: {e}")
        await state.clear()

        # Возвращаемся в меню
        await asyncio.sleep(2)
        await clean_chat_and_restart(message, state)

@router.message(F.text == 'Закрыть смену')
async def close_bd(message: Message):
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

        # Возвращаемся в меню
        await asyncio.sleep(1)
        await clean_chat_and_restart(callback.message, state)
    except Exception as e:
        await callback.message.edit_text(f"Что-то пошло не так, начните заново. Ошибка: {e}")
        await state.clear()

        # Возвращаемся в меню
        await asyncio.sleep(2)
        await clean_chat_and_restart(callback.message, state)

    await callback.answer()

@router.callback_query(lambda c: c.data == "cancel_close_shift")
async def cancel_close_shift(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Закрытие смены отменено")
    await state.clear()
    await callback.answer()

    await asyncio.sleep(1)
    await clean_chat_and_restart(callback.message, state)

    await callback.answer()