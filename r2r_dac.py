import RPi.GPIO as GPIO

class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose=False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial=0)

    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()

    def set_number(self, number):
        if not (0 <= number <= 255):
            print("Число вне 0-255 -> 0")
            number = 0
        bits = [(number >> i) & 1 for i in range(7, -1, -1)]
        GPIO.output(self.gpio_bits, bits)
        if self.verbose:
            print(f"Число: {number}, биты: {bits}")

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение {voltage:.2f} В вне диапазона -> 0")
            voltage = 0.0
        number = int(voltage / self.dynamic_range * 255)
        self.set_number(number)
        if self.verbose:
            print(f"Напряжение: {voltage:.3f} В, код: {number}")

if __name__ == "__main__":
    try:
        dac = R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.2, True)
        while True:
            try:
                voltage = float(input("Введите напряжение: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Ошибка ввода.")
    finally:
        dac.deinit()
