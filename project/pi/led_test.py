import RPi.GPIO as GPIO
import time

RED_PIN   = 23
GREEN_PIN = 24
BLUE_PIN  = 25

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

def set_led(r, g, b):
    GPIO.output(RED_PIN,   GPIO.HIGH if r else GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.HIGH if g else GPIO.LOW)
    GPIO.output(BLUE_PIN,  GPIO.HIGH if b else GPIO.LOW)

try:
    print("RED ON")
    set_led(1, 0, 0)
    time.sleep(2)

    print("GREEN ON")
    set_led(0, 1, 0)
    time.sleep(2)

    print("BLUE ON")
    set_led(0, 0, 1)
    time.sleep(2)

    print("YELLOW (R+G)")
    set_led(1, 1, 0)
    time.sleep(2)

    print("OFF")
    set_led(0, 0, 0)
    time.sleep(1)

finally:
    set_led(0, 0, 0)
    GPIO.cleanup()
    print("GPIO cleanup 완료")