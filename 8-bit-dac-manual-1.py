import RPi.GPIO as GPIO

DAC_BITS = [16, 20, 21, 25, 26, 17, 27, 22]
DYNAMIC_RANGE = 3.2

GPIO.setmode(GPIO.BCM)
for pin in DAC_BITS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

def voltage_to_number(voltage):
    if not (0.0 <= voltage <= DYNAMIC_RANGE):
        print(f"Напряжение вне диапазона (0-{DYNAMIC_RANGE:.2f} В) -> 0")
        return 0
    return int(voltage / DYNAMIC_RANGE * 255)

def number_to_dac(number):
    bits = [(number >> i) & 1 for i in range(7, -1, -1)]
    GPIO.output(DAC_BITS, bits)

try:
    while True:
        try:
            voltage = float(input("Введите напряжение (В): "))
            number_to_dac(voltage_to_number(voltage))
        except ValueError:
            print("Введите число.")
finally:
    GPIO.output(DAC_BITS, 0)
    GPIO.cleanup()
