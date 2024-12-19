import re
import json
from BaseDriver import BaseDriver

class Driver(BaseDriver):
    def __init__(self, last_name, first_name, patronymic, experience, phone_number, birthday, driver_license, vehicle_title, insurance_policy, license_plate, driver_id = None):
        super(Driver, self).__init__(driver_id=driver_id, last_name=last_name, first_name=first_name, patronymic=patronymic, experience=experience)
        self.set_phone_number(phone_number) # Номер телефона
        self.set_birthday(birthday) # Дата рождения
        self.set_driver_license(driver_license) # Водительское удостоверение
        self.set_vehicle_title(vehicle_title) # ПТС
        self.set_insurance_policy(insurance_policy) #С траховой полис
        self.set_license_plate(license_plate) # Номер машины
        
    # Классовый метод создания водителя из JSON
    @classmethod
    def from_json(cls, data_json):
        try:
            data = json.loads(data_json)
            return Driver(
                driver_id=data.get('driver_id'),
                last_name=data['last_name'],
                first_name=data['first_name'],
                patronymic=data['patronymic'],
                experience=data['experience'],

                phone_number=data['phone_number'],
                birthday=data['birthday'],
                driver_license=data['driver_license'],
                vehicle_title=data['vehicle_title'],
                insurance_policy=data['insurance_policy'],
                license_plate=data['license_plate'],
            )
        except KeyError as e:
            raise ValueError(f"Отсутствует обязательный ключ в JSON: {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Ошибка синтаксиса JSON: {e}")
        except Exception as e:
            raise ValueError(f"Некорректные данные в JSON: {e}")

    # Статические методы валидации
    @staticmethod
    def validate_phone_number(phone_number):
        if not isinstance(phone_number, str) or not re.fullmatch(r'((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}', phone_number):
            return False
        return True

    @staticmethod
    def validate_birthday(birthday):
        if not isinstance(birthday, str) or not re.fullmatch(r'\d{2}\.\d{2}\.\d{4}', birthday):
            return False
        return True

    @staticmethod
    def validate_driver_license(driver_license):
        if not isinstance(driver_license, str) or not re.fullmatch(r"^\d{2} \d{2} \d{6}$", driver_license):
            return False
        return True

    @staticmethod
    def validate_vehicle_title(vehicle_title):
        if not isinstance(vehicle_title, str) or not re.fullmatch(r"^\d{2} \d{2} \d{6}$", vehicle_title):
            return False
        return True

    @staticmethod
    def validate_insurance_policy(insurance_policy):
        if not isinstance(insurance_policy, str) or not re.fullmatch(r"^\d{3} \d{12}$", insurance_policy):
            return False
        return True

    @staticmethod
    def validate_license_plate(license_plate):
        if not isinstance(license_plate, str) or not re.fullmatch(r"^[А-Я]{1}\d{3}[А-Я]{2}\s?\d{2,3}$", license_plate):
            return False
        return True

    # Вывод полной версии объекта
    @property
    def full_version(self):
        return (
            f"{self.get_last_name()} {self.get_first_name()} {self.get_patronymic()}",
            self.get_experience(),

            self.get_phone_number(),
            self.get_birthday(),
            self.get_driver_license(),
            self.get_vehicle_title(),
            self.get_insurance_policy(),
            self.get_license_plate(),
            
        )

    # Вывод краткой версии объекта
    @property
    def short_version(self):
        return (
            f"{self.get_last_name()} {self.get_first_name()} {self.get_patronymic()}",
            self.get_experience(),
        )

    # Getters
    def get_phone_number(self):
        return self.__phone_number

    def get_birthday(self):
        return self.__birthday

    def get_driver_license(self):
        return self.__driver_license

    def get_vehicle_title(self):
        return self.__vehicle_title

    def get_insurance_policy(self):
        return self.__insurance_policy

    def get_license_plate(self):
        return self.__license_plate

    # Setters
    def set_phone_number(self, phone_number):
        if super(Driver, self).validate(phone_number, self.validate_phone_number) == False:
            raise ValueError(f"Номер телефона '{phone_number}' некорректен.")
        self.__phone_number = phone_number

    def set_birthday(self, birthday):
        if super(Driver, self).validate(birthday, self.validate_birthday) == False:
            raise ValueError(f"{birthday} должна быть в формате 'ДД.ММ.ГГГГ'.")
        self.__birthday = birthday

    def set_driver_license(self, driver_license):
        if super(Driver, self).validate(driver_license, self.validate_driver_license) == False:
            raise ValueError(f"{driver_license} должен быть в формате 'XX XX XXXXXX'.")
        self.__driver_license = driver_license

    def set_vehicle_title(self, vehicle_title):
        if super(Driver, self).validate(vehicle_title, self.validate_vehicle_title) == False:
            raise ValueError(f"{vehicle_title} должен быть в формате 'XX XX XXXXXX'.")
        self.__vehicle_title = vehicle_title
        
    def set_insurance_policy(self, insurance_policy):
        if super(Driver, self).validate(insurance_policy, self.validate_insurance_policy) == False:
            raise ValueError(f"{insurance_policy} должен быть в формате 'XXX XXXXXXXXXXXX'.")
        self.__insurance_policy = insurance_policy

    def set_license_plate(self, license_plate):
        if super(Driver, self).validate(license_plate, self.validate_license_plate) == False:
            raise ValueError(f"{license_plate} должен быть в формате 'Х111ХХ 111'.")
        self.__license_plate = license_plate