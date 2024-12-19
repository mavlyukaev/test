import json
import yaml
from abc import ABC, abstractmethod
from DriverRepDB import DriverRepDB
from Driver import Driver

# Абстрактный класс для стратегии обработки файлов
class DriverRepStrategy(ABC):
    @abstractmethod
    def read(self, file_path): # Чтение данных из файла
        pass

    @abstractmethod
    def write(self, file_path, data): # Запись данных в файл
        pass

# Стратегия обработки JSON файлов
class JSONStrategy(DriverRepStrategy):
    def read(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def write(self, file_path, data):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

# Стратегия обработки YAML файлов
class YAMLStrategy(DriverRepStrategy):
    def read(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file) or []
        except (FileNotFoundError, yaml.YAMLError):
            return []

    def write(self, file_path, data):
        with open(file_path, 'w', encoding='utf-8') as file:
            yaml.safe_dump(data, file, allow_unicode=True, sort_keys=False)

# Класс дря работы с коллекцией объектов Driver, используя стратегии обработки файлов
class DriverRep:
    def __init__(self, file_path, file_handler: DriverRepStrategy):
        self.file_path = file_path
        self.file_handler = file_handler
        self.drivers = []
        self._read_from_file()

    # Чтение данных из файла с использованием стратегии.
    def _read_from_file(self):
        data = self.file_handler.read(self.file_path)  # Получаем список словарей
        # Преобразуем каждый словарь в строку JSON и передаём в Driver.from_json
        self.drivers = [Driver.from_json(json.dumps(item)) for item in data]

    # Запись данных в файл с использованием стратегии.
    def _write_to_file(self):
        self.file_handler.write(self.file_path, [driver.full_version for driver in self.drivers])

    # Получить объект по ID.
    def get_by_id(self, driver_id):
        for driver in self.drivers:
            if driver.get_driver_id() == driver_id:
                return driver
        raise ValueError(f"Driver с ID {driver_id} не найден.")
    
    # Получить список k по счету n объектов класса short
    def get_k_n_short_list(self, k, n):
        start_index = (k - 1) * n
        end_index = start_index + n
        return [driver.short_version for driver in self.drivers[start_index:end_index]]
    
    # Сортировать элементы по выбранному полю
    def sort_by_field(self, field):
        if not hasattr(Driver, f'get_{field}'):
            raise ValueError(f"Поле {field} не существует в объекте Driver.")
        self.drivers.sort(key=lambda driver: getattr(driver, f'get_{field}')())

    # Добавить объект в список (при добавлении сформировать новый ID)
    def add_driver(self, driver):
        new_id = max((driver.get_driver_id() for driver in self.drivers if driver.get_driver_id()), default=0) + 1
        driver.set_driver_id(new_id)
        self.drivers.append(driver)
        self._write_to_file()

    # Заменить элемент списка по ID.
    def update_driver(self, driver_id, new_driver):
        for i, driver in enumerate(self.drivers):
            if driver.get_driver_id() == driver_id:
                new_driver.set_driver_id(driver_id)  # Сохраняем ID
                self.drivers[i] = new_driver
                self._write_to_file()
                return
        raise ValueError(f"Driver с ID {driver_id} не найден.")
    
    # Удалить элемент списка по ID
    def delete_driver(self, driver_id):
        self.drivers = [driver for driver in self.drivers if driver.get_driver_id() != driver_id]
        self._write_to_file()

    # Получить количество элементов
    def get_count(self):
        return len(self.drivers)
    

class DriverRepDBAdapter:
    def __init__(self, driver_rep_db: DriverRepDB): # Загружаем или инициализируем репозиторий
        self._driver_rep_db = driver_rep_db

    def get_by_id(self, driver_id):
        return self._driver_rep_db.get_by_id(driver_id)
    
    def get_k_n_short_list(self, k, n):
        return self._driver_rep_db.get_k_n_short_list(k, n)

    def add_driver(self, driver):
        self._driver_rep_db.add_driver(driver)

    def update_driver(self, driver_id, new_driver):
        self._driver_rep_db.update_driver(driver_id, new_driver)        

    def delete_driver(self, driver_id):
        self._driver_rep_db.delete_driver(driver_id)

    def get_count(self):
        return self._driver_rep_db.get_count()