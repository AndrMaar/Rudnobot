from aiogram import Router
from aiogram.types import Message
from utils.roles import is_admin
from aiogram.fsm.context import FSMContext
from states.states import OrderRegistration
from aiogram import F
from utils.config import admin_username


router = Router()


@router.message(F.text == 'Показать информацию по водителям')
async def show_stats(message: Message):
    if not is_admin(message.from_user.id) or message.from_user.username == admin_username:
        await message.answer("Эта команда доступна только администраторам.")
        return
        # Запрос статистики из базы данных (пример)
    stats = "Свободные водители: ...\nЗанятые водители: ..."
    await message.answer(stats)



@router.message(F.text == 'Показать историю поездок')
async def show_history(message: Message):
    if not is_admin(message.from_user.id) or message.from_user.username == admin_username:
        await message.answer("Эта команда доступна только администраторам.")
        return

        # Отобразить историю маршрутов
    await message.answer("История маршрутов на карте.")


@router.message(F.text == "Показать статистику")
async def show_state(message: Message):
    if not is_admin(message.from_user.id) or message.from_user.username == admin_username:
        await message.answer("Эта команда доступна только администраторам.")
        return

    await message.answer("Выберите водителя, статистику которого желаете увидеть")
    stats = "Водители: ..."
    await message.answer(stats)


@router.message(F.text == "Зарегистрировать машину")
async def reg_car(message: Message, state: FSMContext):
    if is_admin(message.from_user.id) or message.from_user.username == admin_username:
        await message.answer("Отправьте номер машины")
        await state.set_state(OrderRegistration.wait_car_number)
    else:
        await message.answer("Эта команда доступна только администраторам.")



@router.message(F.text == "Зарегистрировать пользователя")
async def reg_user(message: Message, state: FSMContext):
    if is_admin(message.from_user.id) or message.from_user.username == admin_username:
        await message.answer("Отправьте логин")
        await state.set_state(OrderRegistration.wait_login)
    else:
        await message.answer("Эта команда доступна только администраторам.")








