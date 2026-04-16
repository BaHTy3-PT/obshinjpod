import RPi.GPIO as GPIO

class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verbose=False):
        """
        gpio_pin: номер GPIO-пина (BCM), на котором генерируется ШИМ
        pwm_frequency: частота ШИМ (Гц)
        dynamic_range: максимальное выходное напряжение (В), соответствующее 100% заполнению
        verbose: печатать отладочную информацию
        """
        self.gpio_pin = gpio_pin
        self.pwm_frequency = pwm_frequency
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        # Настройка GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)

        # Создание и запуск PWM-объекта с начальным заполнением 0%
        self.pwm = GPIO.PWM(self.gpio_pin, self.pwm_frequency)
        self.pwm.start(0)

        if self.verbose:
            print(f"PWM DAC инициализирован: пин {self.gpio_pin}, частота {self.pwm_frequency} Гц, диапазон {self.dynamic_range} В")

    def deinit(self):
        """Остановка ШИМ и сброс настроек GPIO"""
        self.pwm.stop()
        GPIO.cleanup(self.gpio_pin)
        if self.verbose:
            print("PWM DAC остановлен, GPIO очищен")

    def set_voltage(self, voltage):
        """
        Установка напряжения на выходе ЦАП (0 – dynamic_range).
        Вычисляет коэффициент заполнения и применяет его к ШИМ.
        """
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение {voltage:.2f} В вне диапазона [0, {self.dynamic_range:.2f}]. Установка 0 В.")
            duty_cycle = 0.0
        else:
            duty_cycle = (voltage / self.dynamic_range) * 100.0

        self.pwm.ChangeDutyCycle(duty_cycle)

        if self.verbose:
            print(f"Установлено напряжение {voltage:.2f} В -> коэффициент заполнения {duty_cycle:.2f}%")

if __name__ == "__main__":
    try:
        # Создаём объект PWM_DAC: пин 12, частота 500 Гц, диапазон 3.290 В (реальное макс. напряжение)
        dac = PWM_DAC(12, 500, 3.290, verbose=True)

        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")

    finally:
        dac.deinit()
