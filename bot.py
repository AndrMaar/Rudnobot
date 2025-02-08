from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from handlers import driver, status, location, registration, admin, start, car_registr
import asyncio
from db.database import init_db
from utils.config import BOT_TOKEN


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрация хэндлеров
    dp.include_router(start.router)
    dp.include_router(status.router)
    dp.include_router(location.router)
    dp.include_router(registration.router)
    dp.include_router(admin.router)
    dp.include_router(driver.router)
    dp.include_router(car_registr.router)

    # Установка команд бота
    await bot.set_my_commands([
        BotCommand(command="start", description="Запуск бота"),
        # BotCommand(command="status", description="Сменить статус"),
        # BotCommand(command="location", description="Отправить локацию"),
        BotCommand(command="registration", description="Зарегистрироваться"),
        BotCommand(command="registration_car", description="Зарегистрировать машину"),
        BotCommand(command="admin", description="Войти как админ"),
        BotCommand(command="driver", description="Войти как водитель")

    ])

    # Инициализация базы данных
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())