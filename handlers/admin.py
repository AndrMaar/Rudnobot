from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from utils.roles import is_admin
from aiogram.filters import Command
from sates.states import OrderRegistration

router = Router()


@router.message(Command('admin'))
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
    await message.answer("Введите ID водителя, чтобы запросить его местоположение.")


@router.message(Command('history'))
async def show_history(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Эта команда доступна только администраторам.")
        return

        # Отобразить историю маршрутов
    await message.answer("История маршрутов на карте.")

@router.message(Command("statistic"))
async def show_stat(message: Message):
    await message.answer("Выберите водителя, статистику которого желаете увидеть")


@router.message(Command("registration_car"))
async def show_stat(message: Message, state: FSMContext):
    await message.answer("Отправте номер машины")
    await state.set_state(OrderRegistration.wait_car_number)