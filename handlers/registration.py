from aiogram import Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from db.database import register_user, check_phone, set_user_by_telegram_id, create_status
from aiogram.filters import Command
from states.states import OrderRegistration
from db.database import get_user_by_telegram_id
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import F
from utils.message_utils import clean_chat_and_restart
import asyncio
from handlers.driver import statuses
from db.database import check_shift_status

router = Router()


@router.message(OrderRegistration.wait_login)
async def login(message: Message, state: FSMContext):
    await state.update_data(login=message.text)
    sent_message = await message.answer("Теперь отправьте номер телефона")

    # Сохраняем ID сообщения
    data = await state.get_data()
    message_ids = data.get("message_ids", [])
    message_ids.append(sent_message.message_id)
    await state.update_data(message_ids=message_ids)

    await state.set_state(OrderRegistration.wait_password)


@router.message(OrderRegistration.wait_password)
async def password(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)

    kb_list = [[KeyboardButton(text="driver")], [KeyboardButton(text='admin')]]
    sent_message = await message.answer('Выберите роль',
                                        reply_markup=ReplyKeyboardMarkup(keyboard=kb_list, one_time_keyboard=True,
                                                                         input_field_placeholder="Выберите роль"))

    # Сохраняем ID сообщения
    data = await state.get_data()
    message_ids = data.get("message_ids", [])
    message_ids.append(sent_message.message_id)
    await state.update_data(message_ids=message_ids)

    await state.set_state(OrderRegistration.wait_choise)


@router.message(OrderRegistration.wait_choise)
async def vib(message: Message, state: FSMContext):
    await state.update_data(role=message.text)
    try:
        data = await state.get_data()
        register_user(telegram_id=None, login=data['login'], phone_number=data['phone_number'],
                      role=data['role'])
        sent_message = await message.answer('Регистрация прошла успешно')

        # Сохраняем ID сообщения
        sent_message = await message.answer('Вы успешно зарегистрировали пользователя')
        data = await state.get_data()
        message_ids = data.get("message_ids", [])
        message_ids.append(sent_message.message_id)
        await state.update_data(message_ids=message_ids)

        # Ждем 2 секунды и возвращаемся в меню
        await asyncio.sleep(2)
        await clean_chat_and_restart(message, state)

    except Exception as e:
        sent_message = await message.answer(f"Что-то пошло не так: {e}")

        # Сохраняем ID сообщения
        data = await state.get_data()
        message_ids = data.get("message_ids", [])
        message_ids.append(sent_message.message_id)
        await state.update_data(message_ids=message_ids)

        await state.clear()

        # Возвращаемся в меню
        await asyncio.sleep(2)
        await clean_chat_and_restart(message, state)

@router.message(OrderRegistration.wait_n)
async def checking(message: Message, state: FSMContext):
    aaaaaa = message.contact.phone_number
    if check_phone(aaaaaa):
        set_user_by_telegram_id(message.from_user.id, aaaaaa)
        user_data = get_user_by_telegram_id(message.from_user.id)
        create_status(status='', user_id=message.chat.id)

        # После регистрации перезапускаем команду start
        await clean_chat_and_restart(message, state)



@router.callback_query(lambda c: c.data == "send_status")
async def process_send_status(callback: CallbackQuery, state: FSMContext):
    if check_shift_status(callback.from_user.id):
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=status, callback_data=f"status_{status}")]
                for status in statuses
            ]
        )
        await callback.message.edit_text("Выберите ваш текущий статус:", reply_markup=keyboard)
    else:
        await callback.message.edit_text("Для отправки статуса необходимо сначала открыть смену.")
        await asyncio.sleep(2)
        await clean_chat_and_restart(callback.message, state)

    await callback.answer()