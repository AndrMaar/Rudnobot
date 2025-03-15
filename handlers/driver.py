from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ContentType
from db.database import save_status, binding, binding_end
from aiogram import F

from utils.roles import is_driver
from utils.config import admin_username

from states.states import OrderRegistration


router = Router()

statuses = ["Погрузка", "Разгрузка", "Обед", "Пересменка", "Заправка", "Ремонт", "Свободен"]

@router.message(F.text == "status")
async def cmd_status(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=status)] for status in statuses],
        resize_keyboard=True
    )
    await message.answer("Выберите ваш текущий статус:", reply_markup=keyboard)

'''
@router.message(F.text == 'location')
async def cmd_location(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Отправить местоположение", request_location=True)]],
        resize_keyboard=True
    )
    await message.answer("Отправьте ваше текущее местоположение:", reply_markup=keyboard)

@router.message(F.content_type == ContentType.LOCATION)
async def handle_location(message: Message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    save_location(user_id=message.from_user.id, latitude=latitude, longitude=longitude)
    await message.answer(f"Ваше местоположение сохранено: {latitude}, {longitude}")
'''

@router.message(lambda msg: msg.text in statuses)
async def handle_status(message: Message):
    selected_status = message.text
    save_status(user_id=message.from_user.id, status=selected_status)
    await message.answer(f"Ваш статус был обновлен: {selected_status}")


@router.message(F.text == 'Открыть смену')
async def open_bd(message: Message, state:FSMContext):
    if is_driver(message.from_user.id) or message.from_user.username == admin_username:
        await message.answer("Отправьте номер машины")
        await state.set_state(OrderRegistration.wait_bd_continue)
    else:
        await message.answer("Эта команда доступна только водителям.")

@router.message(OrderRegistration.wait_bd_continue)
async def open_bd_continue(message: Message,state:FSMContext):
    try:
        binding(telegram_id=message.from_user.id, car_number=message.text)
        await message.answer(f"Готово")
        await state.clear()
    except Exception as e:
        await message.answer(f"Что-то пошло не так, начните заново. Ошибка: {e}")
        await state.clear()


@router.message(F.text == 'Закрыть смену')
async def close_bd(message: Message, state:FSMContext):
    if is_driver(message.from_user.id) or message.from_user.username == admin_username:
        await message.answer("Отправьте номер машины")
        await state.set_state(OrderRegistration.wait_bd_close_continue)
    else:
        await message.answer("Эта команда доступна только водителям.")

@router.message(OrderRegistration.wait_bd_close_continue)
async def open_bd_continue(message: Message,state:FSMContext):
    try:
        binding_end(telegram_id=message.from_user.id, car_number=message.text)
        await message.answer(f"Готово")
        await state.clear()
    except Exception as e:
        await message.answer(f"Что-то пошло не так, начните заново. Ошибка: {e}")
        await state.clear()



