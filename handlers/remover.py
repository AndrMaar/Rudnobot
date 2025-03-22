import asyncio

from aiogram import Router
from aiogram.fsm.context import FSMContext

from db.database import remove_user, remove_car
from states.states import OrderRegistration
from aiogram.types import Message

from utils.message_utils import clean_chat_and_restart

router = Router()

@router.message(OrderRegistration.wait_delete_user)
async def del_user(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    try:
        data = await state.get_data()
        remove_user(phone_number=data['phone_number'])
        sent_message = await message.answer(f"Готово")

        data = await state.get_data()
        message_ids = data.get("message_ids", [])
        message_ids.append(sent_message.message_id)
        await state.update_data(message_ids=message_ids)

        # Возвращаемся в меню
        await asyncio.sleep(2)
        await clean_chat_and_restart(message, state)

    except Exception as e:
        sent_message = await message.answer(f"Что-то пошло не так: {e}")

        data = await state.get_data()
        message_ids = data.get("message_ids", [])
        message_ids.append(sent_message.message_id)
        await state.update_data(message_ids=message_ids)

        # Возвращаемся в меню
        await asyncio.sleep(2)
        await clean_chat_and_restart(message, state)


@router.message(OrderRegistration.wait_delete_car)
async def del_car(message: Message, state: FSMContext):
    await state.update_data(car_number=message.text)
    try:
        data = await state.get_data()
        remove_car(car_number=data['car_number'])
        sent_message = await message.answer(f"Готово")

        data = await state.get_data()
        message_ids = data.get("message_ids", [])
        message_ids.append(sent_message.message_id)
        await state.update_data(message_ids=message_ids)


        # Возвращаемся в меню
        await asyncio.sleep(2)
        await clean_chat_and_restart(message, state)

    except Exception as e:
        sent_message = await message.answer(f"Что-то пошло не так: {e}")

        data = await state.get_data()
        message_ids = data.get("message_ids", [])
        message_ids.append(sent_message.message_id)
        await state.update_data(message_ids=message_ids)


        # Возвращаемся в меню
        await asyncio.sleep(2)
        await clean_chat_and_restart(message, state)






