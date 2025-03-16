from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from db.database import register_car
from states.states import OrderRegistration
from utils.message_utils import clean_chat_and_restart
import asyncio

router = Router()


@router.message(OrderRegistration.wait_car_number)
async def car_number(message: Message, state: FSMContext):
    await state.update_data(car_number=message.text)
    sent_message = await message.answer("Теперь отправьте грузоподъемность")

    # Сохраняем ID сообщения
    data = await state.get_data()
    message_ids = data.get("message_ids", [])
    message_ids.append(sent_message.message_id)
    await state.update_data(message_ids=message_ids)

    await state.set_state(OrderRegistration.wait_max_weight)


@router.message(OrderRegistration.wait_max_weight)
async def max_weight(message: Message, state: FSMContext):
    await state.update_data(max_weight=message.text)
    sent_message = await message.answer("Теперь отправьте марку машины")

    # Сохраняем ID сообщения
    data = await state.get_data()
    message_ids = data.get("message_ids", [])
    message_ids.append(sent_message.message_id)
    await state.update_data(message_ids=message_ids)

    await state.set_state(OrderRegistration.wait_mark)


@router.message(OrderRegistration.wait_mark)
async def name(message: Message, state: FSMContext):
    await state.update_data(mark=message.text)
    sent_message = await message.answer("Теперь отправьте модель машины")

    # Сохраняем ID сообщения
    data = await state.get_data()
    message_ids = data.get("message_ids", [])
    message_ids.append(sent_message.message_id)
    await state.update_data(message_ids=message_ids)

    await state.set_state(OrderRegistration.wait_model)


@router.message(OrderRegistration.wait_model)
async def name(message: Message, state: FSMContext):
    await state.update_data(model=message.text)
    try:
        data = await state.get_data()
        register_car(car_number=data['car_number'], max_weight=data['max_weight'],
                     mark=data['mark'], model=data['model'])

        # Сохраняем ID сообщения
        sent_message = await message.answer('Вы успешно зарегистрировали машину')
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