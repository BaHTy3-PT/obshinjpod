import RPi.GPIO as GPIO

class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose=False):
        """
        gpio_bits: список GPIO-пинов (BCM), подключённых к входам R2R (от младшего бита к старшему)
        dynamic_range: опорное напряжение ЦАП (В), обычно ~3.3 В
        verbose: печатать ли отладочную информацию
        """
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial=0)

    def deinit(self):
        """Сброс GPIO: выходы в 0 и очистка настроек"""
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup(self.gpio_bits)  # очищаем только используемые пины

    def set_number(self, number):
        """Подать целое число (0–255) на вход ЦАП"""
        if not isinstance(number, int):
            raise TypeError("Число должно быть целым")
        if not (0 <= number <= 255):
            raise ValueError("Число выходит за пределы 8-битного диапазона (0–255)")

        # Устанавливаем каждый бит на соответствующем пине
        for i, gpio in enumerate(self.gpio_bits):
            bit = (number >> i) & 1
            GPIO.output(gpio, bit)

        if self.verbose:
            print(f"Установлено число {number} (двоичное: {number:08b})")

    def set_voltage(self, voltage):
        """Выставить напряжение на выходе ЦАП (0 – dynamic_range)"""
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение {voltage:.2f} В выходит за диапазон [0, {self.dynamic_range:.2f}] В. Установка 0 В.")
            number = 0
        else:
            number = int(voltage / self.dynamic_range * 255)
        self.set_number(number)

if __name__ == "__main__":
    try:
        # Пины для R2R (порядок от младшего бита к старшему – согласно схеме)
        dac = R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.183, verbose=True)

        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")
    finally:
        dac.deinit()
