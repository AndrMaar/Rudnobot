import asyncio
from datetime import datetime, timedelta, timezone  # Добавили timezone
from db.database import find_id

async def send(bot):
    while True:
        now = datetime.now(timezone.utc)  # Указали часовой пояс
        next_hour = (now.replace(minute=0, second=0, microsecond=0) + timedelta(minutes=1))
        wait_time = (next_hour - now).total_seconds()
        await asyncio.sleep(wait_time)
        await send_bulk_message(bot)

async def send_bulk_message(bot):
    user_ids = find_id()
    for user_id in user_ids:
        try:
            await bot.send_message(user_id, "Отправьте свой статус")
            await asyncio.sleep(3600)
        except Exception as e:
            print(f"Error sending to {user_id}: {e}")  #





