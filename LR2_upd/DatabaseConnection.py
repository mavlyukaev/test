import sqlite3

# Класс для управления подключением к базе данных (Singleton)
class DatabaseConnection:
    _instance = None

    def __new__(cls, db_path):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._initialize(db_path)
        return cls._instance

    # Инициализация подключения
    def _initialize(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row

    # Возвращает курсор для выполнения SQL-запросов
    def get_cursor(self):
        return self.connection.cursor()

    # Фиксирует изменения в базе данных
    def commit(self):
        self.connection.commit()

    # Закрывает соединение с базой данных и сбрасывает экземпляр класса.
    def close(self):
        self.connection.close()
        DatabaseConnection._instance = None
    
    # Проверяет, существует ли таблица в базе данных
    def table_exists(self, table_name):
        cursor = self.get_cursor()
        cursor.execute("""
            SELECT count(name) 
            FROM sqlite_master 
            WHERE type='table' AND name=?
        """, (table_name,))
        result = cursor.fetchone()
        return result[0] > 0

    # Убеждается, что таблица 'drivers' существует, и создает её при необходимости
    def ensure_table_exists(self):
        if not self.table_exists("drivers"):
            cursor = self.get_cursor()
            cursor.execute("""
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
                );
            """)
            self.commit()
            print("Таблица 'drivers' успешно создана.")
        else:
            print("Таблица 'drivers' уже существует.")