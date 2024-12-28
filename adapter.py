# Старая библиотека с несовместимым интерфейсом
class OldPrinter:
    def specific_print(self, text: str) -> None:
        print(f"Printing from OldPrinter: {text}")

# Новый интерфейс
class Printer:
    def print(self, text: str) -> None:
        raise NotImplementedError

# Адаптер, приводящий старый интерфейс к новому
class PrinterAdapter(Printer):
    def __init__(self, adaptee: OldPrinter):
        self._adaptee = adaptee

    def print(self, text: str) -> None:
        self._adaptee.specific_print(text)

# Клиент, работающий с новым интерфейсом
class Client:
    def __init__(self, printer: Printer):
        self._printer = printer

    def do_print(self, text: str) -> None:
        self._printer.print(text)

# Пример использования
old_printer = OldPrinter()
adapter = PrinterAdapter(old_printer)
client = Client(adapter)

client.do_print("Hello, world!")  # Output: Printing from OldPrinter: Hello, world!