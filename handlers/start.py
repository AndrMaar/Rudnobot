from aiogram import Router
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from states.states import OrderRegistration
from db.database import get_user_by_telegram_id, check_phone, set_user_by_telegram_id, register_user
from aiogram import F
from utils.config import admin_username



router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user_data = get_user_by_telegram_id(message.from_user.id)
    if message.from_user.username == admin_username:
        await message.answer(f"Добрый день")
        kb_list = ([[KeyboardButton(text="Показать информацию по водителям")],
                   [KeyboardButton(text='Показать историю поездок')], [KeyboardButton(text='Показать статистику')],
                   [KeyboardButton(text='Зарегистрировать машину')], [KeyboardButton(text='Зарегистрировать пользователя')],
                   [KeyboardButton(text="Отправить текущий статус")], [KeyboardButton(text="Открыть смену")], [KeyboardButton(text="Закрыть смену")]])
        await message.answer('Теперь вы можете использовать кнопки',
                             reply_markup=ReplyKeyboardMarkup(keyboard=kb_list, one_time_keyboard=True,
                                                              input_field_placeholder="Что вы хотите сделать?"))

    elif user_data:
        login, phone_number, role = user_data
        if role == 'admin':
            await message.answer(f"Добрый день, {login}")
            kb_list = [[KeyboardButton(text="Показать информацию по водителям")], [KeyboardButton(text='Показать историю поездок')],[KeyboardButton(text='Показать статистику')], [KeyboardButton(text='Зарегистрировать машину')], [KeyboardButton(text='Зарегистрировать водителя')]]
            await message.answer('Теперь вы можете использовать кнопки', reply_markup=ReplyKeyboardMarkup(keyboard=kb_list,  one_time_keyboard=True, input_field_placeholder="Что вы хотите сделать?"))
        elif role == 'driver':
            await message.answer(f"Добрый день, {login}")
            kb_list = [[KeyboardButton(text="Отправить текущий статус")], [KeyboardButton(text="Открыть смену")], [KeyboardButton(text="Закрыть смену")]]
            await message.answer('Теперь вы можете использовать кнопки', reply_markup=ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Что вы хотите сделать?"))

    else:
        kb_list = [[KeyboardButton(text="Отправить номер телефона", request_contact=True)]]
        await message.answer('Вам необходимо войти', reply_markup=ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True))
        await state.set_state(OrderRegistration.wait_n)
@router.message(OrderRegistration.wait_n)
async def checking(message: Message, state: FSMContext):
    aaaaaa = message.contact.phone_number
    print(aaaaaa)
    if check_phone(aaaaaa):
        print("1")
        set_user_by_telegram_id(message.from_user.id, aaaaaa)
        user_data = get_user_by_telegram_id(message.from_user.id)
        if user_data:
            login, phone_number, role = user_data
            if role == 'admin':
                await message.answer(f"Добрый день, {login}")
                kb_list = [[KeyboardButton(text="Показать информацию по водителям")], [KeyboardButton(text='Показать историю поездок')],[KeyboardButton(text='Показать статистику')], [KeyboardButton(text='Зарегистрировать машину')], [KeyboardButton(text='Зарегистрировать водителя')]]
                await message.answer('Теперь вы можете использовать кнопки', reply_markup=ReplyKeyboardMarkup(keyboard=kb_list,  one_time_keyboard=True, input_field_placeholder="Что вы хотите сделать?"))
            elif role == 'driver':
                await message.answer(f"Добрый день, {login}")
                kb_list = [[KeyboardButton(text="Отправить текущий статус")], [KeyboardButton(text="Открыть смену")], [KeyboardButton(text="Закрыть смену")]]
                await message.answer('Теперь вы можете использовать кнопки', reply_markup=ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Что вы хотите сделать?"))