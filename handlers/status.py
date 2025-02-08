from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from db.database import save_status
from aiogram.filters import Command

router = Router()

statuses = ["Погрузка", "Разгрузка", "Обед", "Пересменка", "Заправка", "Ремонт"]


@router.message(Command('status'))
async def cmd_status(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=status)] for status in statuses],
        resize_keyboard=True
    )
    await message.answer("Выберите ваш текущий статус:", reply_markup=keyboard)


@router.message(lambda msg: msg.text in statuses)
async def handle_status(message: Message):
    selected_status = message.text
    save_status(user_id=message.from_user.id, status=selected_status)
    await message.answer(f"Ваш статус был обновлен: {selected_status}")