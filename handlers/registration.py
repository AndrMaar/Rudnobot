from aiogram import Router
from aiogram.types import Message
from db.database import register_user
from aiogram.filters import Command
from states.states import OrderRegistration
from db.database import get_user_by_telegram_id
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()


@router.message(OrderRegistration.wait_name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer("теперь отправьте фамилию")
    await state.set_state(OrderRegistration.wait_surname)


@router.message(OrderRegistration.wait_surname)
async def surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)

    await message.answer("теперь отправьте отчество")
    await state.set_state(OrderRegistration.wait_lastname)


@router.message(OrderRegistration.wait_lastname)
async def lastname(message: Message, state: FSMContext):
    await state.update_data(lastname=message.text)

    kb_list = [[KeyboardButton(text="Да"), KeyboardButton(text="Нет")]]
    await message.answer("По умолчанию вам выданы права водителя, хотите ли вы их повысить до прав администратора?", reply_markup=ReplyKeyboardMarkup(keyboard=kb_list))
    await state.set_state(OrderRegistration.yn)


@router.message(OrderRegistration.yn)
async def yn(message: Message, state: FSMContext):
    if message.text == "Да":
        await message.answer("Тогда отправьте пароль администратора следующим сообщением")
        await state.set_state(OrderRegistration.password)
    elif message.text:
        try:
            data = await state.get_data()
            register_user(telegram_id=message.from_user.id, name=data['name'], surname=data['surname'], lastname=data['lastname'])
            await message.answer('Вы успешно зарегестрированы')
            await state.clear()
        except Exception as e:
            await message.answer(f"Что-то пошло не так, начните заново. Ошибка: {e}")
            await state.clear()


@router.message(OrderRegistration.password)
async def password(message: Message, state: FSMContext):
    pass_a = '23456'
    if message.text == pass_a:
        await message.answer("Пароль совпадает")
        try:
            data = await state.get_data()
            register_user(telegram_id=message.from_user.id, name=data['name'], surname=data['surname'], lastname=data['lastname'], role='admin')
            await message.answer('Вы успешно зарегестрированы')
            await state.clear()
        except Exception as e:
            await message.answer(f"Что-то пошло не так, начните заново. Ошибка: {e}")
            await state.clear()

    elif message.text == "Отмена":
        try:
            data = await state.get_data()
            register_user(telegram_id=message.from_user.id, name=data['name'], surname=data['surname'], lastname=data['lastname'])
            await message.answer('Вы успешно зарегестрированы')
            await state.clear()
        except Exception as e:
            await message.answer(f"Что-то пошло не так, начните заново. Ошибка: {e}")
            await state.clear()
    else:
        await message.answer("Пароль неверный. Попробуйте еще раз или напишите \"Отмена\"")