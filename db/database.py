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
                user_id INTEGER NOT NULL,
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
        model TEXT
            )
        ''')
        cursor.execute('''
             CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE NOT NULL,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT "driver"
             )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS car_bindings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        car_id INTEGER,
        user_id TEXT,
        type TEXT,
        FOREIGN KEY (car_id) REFERENCES cars (id)
            )
        ''')


def save_status(user_id, status):
    """Сохраняем статус пользователя в базу данных."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO statuses (user_id, status) VALUES (?, ?)
        ''', (user_id, status))
        conn.commit()


def register_user(telegram_id, name, surname, lastname, role='driver'):
    """Регистрация пользователя."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (telegram_id, name, surname, lastname, role)
            VALUES (?, ?, ?, ?, ?)
        ''', (telegram_id, name, surname, lastname, role))
        conn.commit()


def register_car(car_number, max_weight, mark, model):
    """Регистрация пользователя."""
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
            SELECT name, surname, lastname, role
            FROM users
            WHERE telegram_id = ?
    ''', (telegram_id,))
        return cursor.fetchone()

def get_status():
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()


init_db()