from abc import ABC, abstractmethod

# Базовый компонент
class Coffee(ABC):
    @abstractmethod
    def cost(self) -> float:
        pass

    @abstractmethod
    def description(self) -> str:
        pass

# Конкретный компонент
class SimpleCoffee(Coffee):
    def cost(self) -> float:
        return 5.0

    def description(self) -> str:
        return "Simple Coffee"

# Декоратор
class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee

    def cost(self) -> float:
        return self._coffee.cost()

    def description(self) -> str:
        return self._coffee.description()

# Конкретные декораторы
class MilkDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 1.5

    def description(self) -> str:
        return self._coffee.description() + ", Milk"

class SugarDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.5

    def description(self) -> str:
        return self._coffee.description() + ", Sugar"

# Пример использования
simple_coffee = SimpleCoffee()
print(simple_coffee.description(), "-", simple_coffee.cost())  # Simple Coffee - 5.0

milk_coffee = MilkDecorator(simple_coffee)
print(milk_coffee.description(), "-", milk_coffee.cost())  # Simple Coffee, Milk - 6.5

fancy_coffee = SugarDecorator(milk_coffee)
print(fancy_coffee.description(), "-", fancy_coffee.cost())  # Simple Coffee, Milk, Sugar - 7.0