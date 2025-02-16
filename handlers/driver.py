from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ContentType
from db.database import save_status
from aiogram import F

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





