import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

led = 26
phototransistor = 6

GPIO.setup(led, GPIO.OUT)
GPIO.setup(phototransistor, GPIO.IN)

while True:
    GPIO.output(led, not GPIO.input(phototransistor))
