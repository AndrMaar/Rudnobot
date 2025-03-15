from aiogram import Router
from aiogram.types import Message
from db.database import register_user
from aiogram.filters import Command
from states.states import OrderRegistration
from db.database import get_user_by_telegram_id
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


from aiogram import F


router = Router()


@router.message(OrderRegistration.wait_login)
async def login(message: Message, state: FSMContext):
    await state.update_data(login=message.text)

    await message.answer("Теперь отправьте номер телефона")
    await state.set_state(OrderRegistration.wait_password)
@router.message(OrderRegistration.wait_password)
async def password(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)

    await message.answer("Теперь отправьте роль")
    kb_list = [[KeyboardButton(text="driver")], [KeyboardButton(text='admin')]]
    await message.answer('Выберите роль', reply_markup=ReplyKeyboardMarkup(keyboard=kb_list, one_time_keyboard=True,
                                                                           input_field_placeholder="Выберите роль"))
    await state.set_state(OrderRegistration.wait_choise)
@router.message(OrderRegistration.wait_choise)
async def vib(message: Message, state: FSMContext):
    await state.update_data(role=message.text)

    try:
        data = await state.get_data()
        register_user(telegram_id= '', login=data['login'], phone_number=data['phone_number'], role=data['role'])
        await message.answer('Регистрация прошла успешно')
        await state.clear()
    except Exception as e:
        await message.answer(f"Что-то пошло не так, начните заново. Ошибка: {e}")
        await state.clear()