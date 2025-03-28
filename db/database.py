import sqlite3
from multiprocessing.forkserver import connect_to_new_process

from utils.config import DATABASE_PATH

#conn = sqlite3.connect("cars.db")
#cursor = conn.cursor()

def init_db():
    """Создаем таблицы, если их еще нет."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS statuses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                status TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        car_number TEXT UNIQUE,
        max_weight REAL,
        mark TEXT,
        model TEXT,
        is_busy INTEGER DEFAULT 0
            )
        ''')
        cursor.execute('''
             CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                login TEXT NOT NULL,
                phone_number TEXT UNIQUE NOT NULL,
                role TEXT NOT NULL ,
                is_busy INTEGER DEFAULT 0
             )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS car_bindings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER,
        car_number INTEGER
            )
        ''')


def create_status(user_id, status):
    """Сохраняем статус пользователя в базу данных."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO statuses (user_id, status) VALUES (?, ?)
        ''', (user_id, status))
        conn.commit()

def save_status(status, user_id):
    """Сохраняем статус пользователя в базу данных."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE statuses
            SET status = ?
            WHERE user_id = ?
        ''', (status, user_id,))
        conn.commit()


def register_user(telegram_id, login, phone_number, role):
    """Регистрация пользователя"""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (telegram_id, login, phone_number, role)
            VALUES (?, ?, ?, ?)
        ''', (telegram_id, login, phone_number, role))
        conn.commit()


def register_car(car_number, max_weight, mark, model):
    """Регистрация машины"""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cars (car_number, max_weight, mark, model)
            VALUES (?, ?, ?, ?)
        ''', (car_number, max_weight, mark, model))
        conn.commit()

def get_user_by_telegram_id(telegram_id):
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
                SELECT login, phone_number, role
                FROM users
                WHERE telegram_id = ?
        ''', (telegram_id,))
        return cursor.fetchone()


def check_phone(phone_number):
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
                SELECT phone_number
                FROM users
                WHERE phone_number = ?
        ''', (str(phone_number),))
        return cursor.fetchone()

def check_shift_status(telegram_id):
    """Проверяет, открыта ли смена у водителя"""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT is_busy
            FROM users
            WHERE telegram_id = ?
        ''', (telegram_id,))
        result = cursor.fetchone()
        return result and result[0] == 1


def find_id():
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT telegram_id 
            FROM users 
            WHERE role = 'driver'
        ''')
        return [row[0] for row in cursor.fetchall()]  # Получаем все ID


def set_user_by_telegram_id(telegram_id, phone):
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users 
            SET telegram_id = ? 
            WHERE phone_number = ? 
    ''', (telegram_id, phone))
        return cursor.fetchone()

def binding(telegram_id, car_number):
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()

            cursor.execute('SELECT is_busy FROM cars WHERE car_number = ?', (car_number,))
            car_status = cursor.fetchone()
            if car_status and car_status[0] == 1:
                raise ValueError(f"Car {car_number} is already busy.")

            cursor.execute('SELECT is_busy FROM users WHERE telegram_id = ?', (telegram_id,))
            user_status = cursor.fetchone()
            if user_status and user_status[0] == 1:
                raise ValueError(f"User {telegram_id} is already busy.")

            cursor.execute('''
                   INSERT INTO car_bindings (telegram_id, car_number)
                   VALUES (?, ?)
               ''', (telegram_id, car_number))
            cursor.execute('''
                   UPDATE cars
                   SET is_busy = 1
                   WHERE car_number = ?
               ''', (car_number,))
            cursor.execute('''
                  UPDATE users 
                  SET is_busy = 1
                  WHERE telegram_id = ?
              ''', (telegram_id,))
            conn.commit()


    except (sqlite3.Error, ValueError) as e:
        conn.rollback()
        print(f"Error: {e}")

def binding_end(telegram_id):
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
               SELECT car_number 
               from car_bindings
               WHERE telegram_id = ?
           ''', (telegram_id,))
        car_record = cursor.fetchone()

        cursor.execute('''
               UPDATE cars 
               SET is_busy = 0
               WHERE car_number = ?
           ''', (car_record[0],))
        cursor.execute('''
              DELETE FROM car_bindings 
              WHERE telegram_id = ?
           ''', (telegram_id,))

        cursor.execute('''
               UPDATE users 
               SET is_busy = 0
               WHERE telegram_id = ?
           ''', (telegram_id,))
        conn.commit()


def remove_user(phone_number):
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM users 
            WHERE phone_number = ? 
    ''', (phone_number,))
        conn.commit()

def remove_car(car_number):
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM cars 
            WHERE car_number = ? 
    ''', (car_number,))
        conn.commit()

def drivers_list():
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT login
        FROM users
        WHERE role=\'driver\' AND is_busy=1''')
        return  cursor.fetchall()

def cars_list():
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT car_number
        FROM cars
        WHERE is_busy=1''')
        return  cursor.fetchall()

def get_driver_statuses(driver):
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT status, timestamp
        FROM statuses
        WHERE user_id = (
        SELECT telegram_id
        FROM users
        WHERE login=?)
        LIMIT 5''', (driver, ))
        return cursor.fetchall()

def get_car_statuses(car_number):
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT status, timestamp
        FROM statuses
        WHERE user_id = (
        SELECT telegram_id
        FROM car_bindings
        WHERE car_number=?)''', (car_number, ))
        return cursor.fetchall()

init_db()