import RPi.GPIO as GPIO

# Пины R2R (BCM, от младшего бита к старшему)
DAC_BITS = [16, 20, 21, 25, 26, 17, 27, 22]
DYNAMIC_RANGE = 3.183  # Вольт

GPIO.setmode(GPIO.BCM)
GPIO.setup(DAC_BITS, GPIO.OUT, initial=0)

def voltage_to_number(voltage):
    if not (0.0 <= voltage <= DYNAMIC_RANGE):
        print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {DYNAMIC_RANGE:.2f} В)")
        print("Устанавливаем 0.0 В")
        return 0
    return int(voltage / DYNAMIC_RANGE * 255)

def number_to_dac(number):
    for i, gpio in enumerate(DAC_BITS):
        bit = (number >> i) & 1
        GPIO.output(gpio, bit)

try:
    while True:
        try:
            voltage = float(input("Введите напряжение в Вольтах: "))
            number = voltage_to_number(voltage)
            number_to_dac(number)
        except ValueError:
            print("Вы ввели не число. Попробуйте ещё раз\n")
finally:
    GPIO.output(DAC_BITS, 0)
    GPIO.cleanup()
