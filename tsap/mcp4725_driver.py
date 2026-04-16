import smbus

class MCP4725:
    def __init__(self, dynamic_range, address=0x61, verbose=True):
        self.bus = smbus.SMBus(1)          # шина I2C на Raspberry Pi (1 для Rev.2)
        self.address = address
        self.wm = 0x00                     # быстрый режим записи (без EEPROM)
        self.pds = 0x00                    # нормальный режим работы
        self.verbose = verbose
        self.dynamic_range = dynamic_range

    def deinit(self):
        """Закрыть I2C шину"""
        self.bus.close()

    def set_number(self, number):
        """Установить 12-битное число (0–4095) на выход ЦАП"""
        if not isinstance(number, int):
            print("На вход ЦАП можно подавать только целые числа")
            return
        if not (0 <= number <= 4095):
            print("Число выходит за разрядность MCP4725 (12 бит)")
            return

        # Первый байт: старшие 4 бита числа + биты конфигурации
        first_byte = (self.wm << 4) | (self.pds << 2) | (number >> 8)
        # Второй байт: младшие 8 бит
        second_byte = number & 0xFF

        # Отправка двух байт данных по I2C (адрес 0x61, первый байт как command)
        self.bus.write_byte_data(self.address, first_byte, second_byte)

        if self.verbose:
            print(f"Число: {number}, отправленные по I2C данные: [0x{(self.address << 1):02X}, 0x{first_byte:02X}, 0x{second_byte:02X}]\n")

    def set_voltage(self, voltage):
        """Выставить напряжение (0 – dynamic_range) на выходе ЦАП"""
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение {voltage:.2f} В вне диапазона [0, {self.dynamic_range:.2f}]. Установка 0 В.")
            number = 0
        else:
            # Преобразование напряжения в 12-битное число
            number = int(voltage / self.dynamic_range * 4095)
        self.set_number(number)


if __name__ == "__main__":
    try:
        # Создаём объект MCP4725 с диапазоном 5.0 В, адрес по умолчанию 0x61
        dac = MCP4725(dynamic_range=5.0, address=0x61, verbose=True)

        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")

    finally:
        dac.deinit()
