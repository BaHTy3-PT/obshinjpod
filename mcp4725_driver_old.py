import smbus

class MCP4725:
    def __init__(self, dynamic_range, address=0x61, verbose=False):
        self.bus = smbus.SMBus(1)
        self.address = address
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        # Настройки: режим быстрого записи (fast mode), обычное питание
        self.config = 0x00   # bits: C2=0, C1=0, PD0=0

    def deinit(self):
        self.bus.close()

    def set_number(self, number):
        """Записать 12-битное число (0..4095) в ЦАП"""
        if not isinstance(number, int):
            print("Ошибка: число должно быть целым")
            return
        if not (0 <= number <= 4095):
            print("Число вне диапазона 0..4095, устанавливаем 0")
            number = 0
        # Формируем два байта: первый – старшие 4 бита числа + конфиг, второй – младшие 8 бит
        first_byte = (self.config << 4) | (number >> 8)
        second_byte = number & 0xFF
        self.bus.write_byte_data(self.address, first_byte, second_byte)
        if self.verbose:
            print(f"Число: {number} → байты: [0x{first_byte:02X}, 0x{second_byte:02X}]")

    def set_voltage(self, voltage):
        if not isinstance(voltage, (int, float)):
            print("Напряжение должно быть числом")
            return
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение {voltage:.2f} В вне диапазона (0-{self.dynamic_range:.2f}) -> 0 В")
            voltage = 0.0
        number = round(voltage / self.dynamic_range * 4095)
        self.set_number(number)
        if self.verbose:
            print(f"Напряжение: {voltage:.3f} В, код: {number}")

if __name__ == "__main__":
    dac = None
    try:
        dac = MCP4725(5.0, address=0x61, verbose=True)
        while True:
            try:
                voltage = float(input("Введите напряжение (0-5.0 В): "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Ошибка ввода.")
    finally:
        if dac:
            dac.deinit()
