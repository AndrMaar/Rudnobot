import asyncio
from datetime import datetime, timedelta
from db.database import find_id



async def send(bot):
    while True:

        now = datetime.now()
        next_hour = (now.replace(minute=0, second=0, microsecond=0) + timedelta(minutes=1))
        wait_time = (next_hour - now).total_seconds()

        # Ожидаем до следующего часа
        await asyncio.sleep(wait_time)

        # Отправляем рассылку
        await send_bulk_message(bot)

async def send_bulk_message(bot):
    user_ids = find_id()
    for user_id in user_ids:
        try:
            await bot.send_message(user_id, "Отправьте свой статус")
        except Exception as e:
            print(e)







