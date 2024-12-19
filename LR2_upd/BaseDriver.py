import re

class BaseDriver:
    def __init__(self, driver_id, last_name, first_name, patronymic, experience):
        self.__driver_id = None
        self.set_driver_id(driver_id)
        self.set_last_name(last_name)
        self.set_first_name(first_name)
        self.set_patronymic(patronymic)
        self.set_experience(experience)

    # Общий метод валидации
    @staticmethod
    def validate(value, validation_function):
        return validation_function(value)

    # Статические методы валидации
    @staticmethod
    def validate_driver_id(driver_id):
        if not isinstance(driver_id, int) or driver_id <= 0:
            return False
        return True
    
    @staticmethod
    def validate_last_name(last_name):
        if not isinstance(last_name, str) or len(last_name.strip()) == 0:
            return False
        return True

    @staticmethod
    def validate_first_name(first_name):
        if not isinstance(first_name, str) or len(first_name.strip()) == 0:
            return False
        return True

    @staticmethod
    def validate_patronymic(patronymic):
        if not isinstance(patronymic, str) or len(patronymic.strip()) == 0:
            return False
        return True

    @staticmethod
    def validate_experience(experience):
        if not isinstance(experience, int) or experience < 0:
            return False
        return True

    # Метод сравнения объектов на равенство (сравнение всех полей)
    def __eq__(self, other):
        return (
            self.get_driver_id() == other.get_driver_id()
            and self.get_last_name() == other.get_last_name()
            and self.get_first_name() == other.get_first_name()
            and self.get_patronymic() == other.get_patronymic()
            and self.get_experience() == other.get_experience()
        )

    def __ne__(self, other):
        return not (self.__eq__(other))

    def __hash__(self):
        return hash(
            (
                self.get_driver_id(),
                self.get_last_name(),
                self.get_first_name(),
                self.get_patronymic(),
                self.get_experience(),
            )
        )

    # Метод вывода str
    def __str__(self):
        return (
            f"Driver ID: {self.get_driver_id()}, Name: {self.get_last_name()} "
            f"{self.get_first_name()} {self.get_patronymic()}, Experience: {self.get_experience()} years"
        )

    # Метод вывода repr
    def __repr__(self):
        return (
            f"Driver(driver_id={self.get_driver_id()}, last_name='{self.get_last_name()}', "
            f"first_name='{self.get_first_name()}', patronymic='{self.get_patronymic()}', "
            f"experience={self.get_experience()})"
        )

    # Getters
    def get_driver_id(self):
        return self.__driver_id

    def get_last_name(self):
        return self.__last_name

    def get_first_name(self):
        return self.__first_name

    def get_patronymic(self):
        return self.__patronymic

    def get_experience(self):
        return self.__experience

    # Setters
    def set_driver_id(self, driver_id):
        if driver_id is not None and (not isinstance(driver_id, int) or driver_id <= 0):
            raise ValueError("ID должно быть положительным числом.")
        self.__driver_id = driver_id

    def set_last_name(self, last_name):
        if not self.validate(last_name, self.validate_last_name):
            raise ValueError("Строка не может быть пустой.")
        self.__last_name = last_name

    def set_first_name(self, first_name):
        if not self.validate(first_name, self.validate_first_name):
            raise ValueError("Строка не может быть пустой.")
        self.__first_name = first_name

    def set_patronymic(self, patronymic):
        if not self.validate(patronymic, self.validate_patronymic):
            raise ValueError("Строка не может быть пустой.")
        self.__patronymic = patronymic

    def set_experience(self, experience):
        if not self.validate(experience, self.validate_experience):
            raise ValueError("Стаж не может быть меньше 0.")
        self.__experience = experience