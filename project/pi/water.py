import RPi.GPIO as GPIO
from time import sleep

WATER_SENSOR_PIN = 12

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(WATER_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    while True:
        print(GPIO.input(WATER_SENSOR_PIN))
        sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()