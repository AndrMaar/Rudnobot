from db.database import get_user_by_telegram_id


def is_admin(telegram_id):
    user = get_user_by_telegram_id(telegram_id)
    return user and user[3] == "admin"

def is_driver(telegram_id):
    user = get_user_by_telegram_id(telegram_id)
    return user and user[3] == "driver"