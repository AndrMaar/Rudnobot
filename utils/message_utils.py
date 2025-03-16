import asyncio
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from handlers.start import cmd_start

async def send_and_delete(message: Message, text: str, reply_markup=None, delete_after=5, delete_original=True,
                          state: FSMContext = None):
    """
    Отправляет сообщение и удаляет его через указанное время.

    :param message: Оригинальное сообщение
    :param text: Текст сообщения
    :param reply_markup: Клавиатура (опционально)
    :param delete_after: Время в секундах до удаления (0 - не удалять)
    :param delete_original: Удалять ли оригинальное сообщение
    :param state: Объект FSMContext для сохранения ID сообщений
    """
    # Удаляем оригинальное сообщение пользователя
    if delete_original:
        try:
            await message.delete()
        except Exception as e:
            print(f"Не удалось удалить сообщение: {e}")

    # Отправляем новое сообщение
    sent_message = await message.answer(text, reply_markup=reply_markup)

    # Сохраняем ID в состоянии
    if state:
        data = await state.get_data()
        message_ids = data.get("message_ids", [])
        message_ids.append(sent_message.message_id)
        await state.update_data(message_ids=message_ids)

    # Запускаем таймер для удаления
    if delete_after > 0:
        async def delete_later():
            await asyncio.sleep(delete_after)
            try:
                await message.bot.delete_message(message.chat.id, sent_message.message_id)
            except Exception as e:
                print(f"Не удалось удалить сообщение: {e}")

        await asyncio.create_task(delete_later())

    return sent_message.message_id


async def clean_chat_and_restart(message, state: FSMContext = None):
    """
    Очищает чат от предыдущих сообщений и вызывает команду /start
    """
    # Удаляем сохраненные сообщения из состояния
    if state:
        data = await state.get_data()
        message_ids = data.get("message_ids", [])
        for message_id in message_ids:
            try:
                await message.bot.delete_message(message.chat.id, message_id)
            except Exception as e:
                print(f"Ошибка удаления сообщения {message_id}: {e}")
        # Очищаем список сообщений
        await state.update_data(message_ids=[])

    # Вызываем команду start

    await cmd_start(message, state)









