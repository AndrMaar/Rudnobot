from aiogram import Router
from aiogram.types import Message
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
        if role == 'driver':
            await message.answer(
                f"Добрый день, {name} {lastname}\nДля изменения статуса вы можете использовать команду \n/status,\n/location")
        elif role == 'admin':
            await message.answer(
                f"Добрый день, {name} {lastname}\nКоманды администратора: \n/drivers_info,\n/request_location,\n/history,\n/statistic,\n/registration_car,\n/create_bind")
    else:
        await message.answer("Вам необходимо зарегистрироваться. Для начала отправьте мне ваше имя (например Иван)")
        await state.set_state(OrderRegistration.wait_name)
