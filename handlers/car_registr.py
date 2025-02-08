from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from db.database import register_car
from sates.states import OrderRegistration

router = Router()

@router.message(OrderRegistration.wait_car_number)
async def car_number(message: Message, state: FSMContext):
    await state.update_data(car_number=message.text)
    await message.answer("теперь отправьте номер машины")
    await state.set_state(OrderRegistration.wait_max_weight)

@router.message(OrderRegistration.wait_max_weight)
async def max_weight(message: Message, state: FSMContext):
    await state.update_data(max_weight=message.text)
    await message.answer("теперь отправьте грузоподъемность")
    await state.set_state(OrderRegistration.wait_mark)

@router.message(OrderRegistration.wait_mark)
async def name(message: Message, state: FSMContext):
    await state.update_data(mark=message.text)
    await message.answer("теперь отправьте имя")
    await state.set_state(OrderRegistration.wait_model)

@router.message(OrderRegistration.wait_model)
async def name(message: Message, state: FSMContext):
    await state.update_data(model=message.text)
    await message.answer("теперь отправьте имя")
    try:
        data = await state.get_data()
        register_car(car_number=data['car_number'], max_weight=data['max_weight'], mark=data['mark'],model=data['model'])
        await message.answer('Вы успешно зарегестрированы')
        await state.clear()
    except:
        await message.answer("Что-то пошло не так, начните заново")
        await state.clear()




