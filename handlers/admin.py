from aiogram import Router
from aiogram.types import Message
from utils.roles import is_admin
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.states import OrderRegistration


router = Router()


@router.message(Command('drivers_info'))
async def show_stats(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Эта команда доступна только администраторам.")
        return

        # Запрос статистики из базы данных (пример)
    stats = "Свободные водители: ...\nЗанятые водители: ..."
    await message.answer(stats)


@router.message(Command('request_location'))
async def request_location(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Эта команда доступна только администраторам.")
        return

        # Реализация запроса локации у водителя
    await message.answer("Выберите водителя, чтобы запросить его местоположение.")
    stats = "Водители: ..."
    await message.answer(stats)


@router.message(Command('history'))
async def show_history(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Эта команда доступна только администраторам.")
        return

        # Отобразить историю маршрутов
    await message.answer("История маршрутов на карте.")


@router.message(Command("statistic"))
async def show_stat(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Эта команда доступна только администраторам.")
        return

    await message.answer("Выберите водителя, статистику которого желаете увидеть")
    stats = "Водители: ..."
    await message.answer(stats)


@router.message(Command("registration_car"))
async def reg_car(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("Эта команда доступна только администраторам.")
        return

    await message.answer("Отправьте номер машины")
    await state.set_state(OrderRegistration.wait_car_number)


@router.message(Command('create_bind'))
async def create_bd(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Эта команда доступна только администраторам.")
        return

    await message.answer("Укажите водителя и машину которая будет ему назначена")
    stats = "Водители: ...\n Машины: ..."
    await message.answer(stats)