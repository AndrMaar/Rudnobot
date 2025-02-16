from aiogram import Router
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from states.states import OrderRegistration
from db.database import get_user_by_telegram_id

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user_data = get_user_by_telegram_id(message.from_user.id)
    if user_data:
        name, surname, lastname, role = user_data
        if role == 'admin':
            await message.answer(f"Добрый день, {name} {lastname}")
            kb_list = [[KeyboardButton(text="Показать информацию по водителям")], [KeyboardButton(text='Показать историю поездок')],
                        [KeyboardButton(text='Показать статистику')], [KeyboardButton(text='Зарегистрировать машину')], [KeyboardButton(text='Привязать машину к водителю')]]
            await message.answer('Теперь вы можете использовать кнопки', reply_markup=ReplyKeyboardMarkup(keyboard=kb_list,  one_time_keyboard=True, input_field_placeholder="Что вы хотите сделать?"))

        elif role == 'driver':
            await message.answer(f"Добрый день, {name} {lastname}")
            kb_list = [[KeyboardButton(text="Отправить текущий статус")]]
            await message.answer('Теперь вы можете использовать кнопки', reply_markup=ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Что вы хотите сделать?"))
    else:
        await message.answer("Вам необходимо зарегистрироваться. Для начала отправьте мне ваше имя (например Иван)")
        await state.set_state(OrderRegistration.wait_name)
