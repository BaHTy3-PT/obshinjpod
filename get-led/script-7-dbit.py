import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

leds = [16, 12, 25, 17, 27, 23, 22, 24]

up = 9      
down = 10  

GPIO.setup(leds, GPIO.OUT)
GPIO.output(leds, 0)

GPIO.setup(up, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(down, GPIO.IN, pull_up_down=GPIO.PUD_UP)

num = 0
sleep_time = 0.2          

def dec2bin(value):
    """Преобразует число 0-255 в список битов (старший бит первый)"""
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

try:
    while True:
        
        up_pressed = (GPIO.input(up) == 0)
        down_pressed = (GPIO.input(down) == 0)

        if up_pressed and down_pressed:
           
            num = 255
            print("MAX:", num, dec2bin(num))
            time.sleep(sleep_time)
          
            while GPIO.input(up) == 0 or GPIO.input(down) == 0:
                time.sleep(0.01)
        elif up_pressed:
           
            num = (num + 1) % 256
            print(num, dec2bin(num))
            time.sleep(sleep_time)
            while GPIO.input(up) == 0:
                time.sleep(0.01)
        elif down_pressed:
          
            num = (num - 1) % 256
            print(num, dec2bin(num))
            time.sleep(sleep_time)
            while GPIO.input(down) == 0:
                time.sleep(0.01)

        GPIO.output(leds, dec2bin(num))
        time.sleep(0.02)

except KeyboardInterrupt:
    GPIO.output(leds, 0)
    GPIO.cleanup()
