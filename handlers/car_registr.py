from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from db.database import register_car
from sates.states import OrderRegistration

router = Router()

@router.message(OrderRegistration.wait_car_number)
async def car_number(message: Message, state: FSMContext):
    await state.update_data(car_number=message.text)
    await state.set_state(OrderRegistration.wait_max_weight)

    await message.answer("Теперь отправьте грузоподъемность")
    await state.set_state(OrderRegistration.wait_max_weight)
@router.message(OrderRegistration.wait_max_weight)
async def max_weight(message: Message, state: FSMContext):
    await state.update_data(max_weight=message.text)

    await message.answer("Теперь отправьте марку машины")
    await state.set_state(OrderRegistration.wait_mark)
@router.message(OrderRegistration.wait_mark)
async def car_mark(message: Message, state: FSMContext):
    await state.update_data(mark=message.text)

    await message.answer("Теперь отправьте модель машины")
    await state.set_state(OrderRegistration.wait_model)
@router.message(OrderRegistration.wait_model)
async def car_model(message: Message, state: FSMContext):
    await state.update_data(model=message.text)
    try:
        data = await state.get_data()
        register_car(car_number=data['car_number'], max_weight=data['max_weight'], mark=data['mark'],model=data['model'])
        await message.answer('Вы успешно зарегестрированы')
        await state.clear()
    except:
        await message.answer("Что-то пошло не так, начните заново")
        await state.clear()




