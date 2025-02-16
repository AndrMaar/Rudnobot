from aiogram import Router
from aiogram.types import Message
from utils.roles import is_admin
from aiogram.fsm.context import FSMContext
from states.states import OrderRegistration
from aiogram import F


router = Router()


@router.message(F.text == 'drivers_info')
async def show_stats(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Эта команда доступна только администраторам.")
        return

        # Запрос статистики из базы данных (пример)
    stats = "Свободные водители: ...\nЗанятые водители: ..."
    await message.answer(stats)



@router.message(F.text == 'history')
async def show_history(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Эта команда доступна только администраторам.")
        return

        # Отобразить историю маршрутов
    await message.answer("История маршрутов на карте.")


@router.message(F.text == "statistic")
async def show_stat(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Эта команда доступна только администраторам.")
        return

    await message.answer("Выберите водителя, статистику которого желаете увидеть")
    stats = "Водители: ..."
    await message.answer(stats)


@router.message(F.text == "registration_car")
async def reg_car(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("Эта команда доступна только администраторам.")
        return

    await message.answer("Отправьте номер машины")
    await state.set_state(OrderRegistration.wait_car_number)


@router.message(F.text == 'create_bind')
async def create_bd(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Эта команда доступна только администраторам.")
        return

    await message.answer("Укажите водителя и машину которая будет ему назначена")
    stats = "Водители: ...\n Машины: ..."
    await message.answer(stats)