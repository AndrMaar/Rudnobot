from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command('driver'))
async def set_status(message: Message):
    await message.answer("Укажите ваш статус (например, Погрузка, Разгрузка).")
    # Реализация аналогична предыдущему кейсу


@router.message(Command('location'))
async def send_location(message: Message):
    await message.answer("Отправьте свое местоположение.")
    # Реализация аналогична предыдущему кейсу





