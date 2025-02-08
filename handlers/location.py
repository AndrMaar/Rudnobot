from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ContentType
from db.database import save_location
from aiogram.filters import Command
from aiogram import F

router = Router()


@router.message(Command('location'))
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