import sqlite3
from DatabaseConnection import DatabaseConnection
from Driver import Driver

class DriverRepDB:
    def __init__(self, db_path):
        self.db_path = db_path
        self._initialize_database()

    # Инициализация базы данных
    def _initialize_database(self):
        db = DatabaseConnection(self.db_path)
        cursor = db.get_cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS drivers (
                driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
                last_name TEXT NOT NULL,
                first_name TEXT NOT NULL,
                patronymic TEXT NOT NULL,
                experience INTEGER NOT NULL,
                phone_number TEXT NOT NULL,
                birthday TEXT NOT NULL,
                driver_license TEXT NOT NULL,
                vehicle_title TEXT NOT NULL,
                insurance_policy TEXT NOT NULL,
                license_plate TEXT NOT NULL
            )
        ''')
        db.commit()

    # Получить объект по ID
    def get_by_id(self, driver_id):
            db = DatabaseConnection(self.db_path)
            cursor = db.get_cursor()
            cursor.execute("SELECT * FROM drivers WHERE driver_id = ?", (driver_id,))
            row = cursor.fetchone()
            if row:
                # Создание объекта Driver с правильным использованием геттеров
                return Driver(
                    driver_id=row[0],
                    last_name=row[1],
                    first_name=row[2],
                    patronymic=row[3],
                    experience=row[4],
                    phone_number=row[5],
                    birthday=row[6],
                    driver_license=row[7],
                    vehicle_title=row[8],
                    insurance_policy=row[9],
                    license_plate=row[10]
                )
            raise ValueError(f"Driver с ID {driver_id} не найден.")

    # Получить список k по счету n объектов класса short
    def get_k_n_short_list(self, k, n):
            offset = (k - 1) * n
            db = DatabaseConnection(self.db_path)
            cursor = db.get_cursor()
            cursor.execute("SELECT last_name, first_name, patronymic, experience FROM drivers LIMIT ? OFFSET ?", (n, offset))
            return [f"{row[0]} {row[1]} {row[2]} ({row[3]} лет стажа)" for row in cursor.fetchall()]
    
    # Добавить объект в список (при добавлении сформировать новый ID)
    def add_driver(self, driver):
            db = DatabaseConnection(self.db_path)
            cursor = db.get_cursor()
            cursor.execute('''
                INSERT INTO drivers (
                    last_name, first_name, patronymic, experience, phone_number, birthday,
                    driver_license, vehicle_title, insurance_policy, license_plate
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                driver.get_last_name(), driver.get_first_name(), driver.get_patronymic(), driver.get_experience(),
                driver.get_phone_number(), driver.get_birthday(), driver.get_driver_license(),
                driver.get_vehicle_title(), driver.get_insurance_policy(), driver.get_license_plate()
            ))
            db.commit()
            driver.set_driver_id(cursor.lastrowid)
    
    # Заменить элемент списка по ID
    def update_driver(self, driver_id, new_driver):
            db = DatabaseConnection(self.db_path)
            cursor = db.get_cursor()
            cursor.execute('''
                UPDATE drivers SET
                    last_name = ?, first_name = ?, patronymic = ?, experience = ?,
                    phone_number = ?, birthday = ?, driver_license = ?, vehicle_title = ?,
                    insurance_policy = ?, license_plate = ?
                WHERE driver_id = ?
            ''', (
                new_driver.get_last_name(), new_driver.get_first_name(), new_driver.get_patronymic(),
                new_driver.get_experience(), new_driver.get_phone_number(), new_driver.get_birthday(),
                new_driver.get_driver_license(), new_driver.get_vehicle_title(),
                new_driver.get_insurance_policy(), new_driver.get_license_plate(), driver_id
            ))
            if cursor.rowcount == 0:
                raise ValueError(f"Driver с ID {driver_id} не найден.")
            db.commit()

    # Удалить элемент списка по ID
    def delete_driver(self, driver_id):
            db = DatabaseConnection(self.db_path)
            cursor = db.get_cursor()
            cursor.execute("DELETE FROM drivers WHERE driver_id = ?", (driver_id,))
            if cursor.rowcount == 0:
                raise ValueError(f"Driver с ID {driver_id} не найден.")
            db.commit()

    # Получить количество элементов
    def get_count(self):
            db = DatabaseConnection(self.db_path)
            cursor = db.get_cursor()
            cursor.execute("SELECT COUNT(*) FROM drivers")
            return cursor.fetchone()[0]
