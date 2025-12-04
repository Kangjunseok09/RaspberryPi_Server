import RPi.GPIO as GPIO
import time

BUZZER_PIN = 10  # 형님 GPIO 번호로 변경

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

pwm = GPIO.PWM(BUZZER_PIN, 1000)  # 기본 주파수
pwm.start(0)  # 처음엔 OFF

def beep(freq, duration):
    pwm.ChangeFrequency(freq)
    pwm.start(50)  # 소리 켜기
    time.sleep(duration)
    pwm.stop()  # 소리 끄기

def stage_normal():
    print("Stage 1 - Normal (No sound)")
    pwm.stop()
    time.sleep(1)

def stage_warning():
    print("Stage 2 - Warning (삐삐삐)")
    for _ in range(3):
        beep(2000, 0.2)
        time.sleep(0.2)

def stage_danger():
    print("Stage 3 - Danger (긴 삐—)")
    beep(3000, 1.0)
    time.sleep(1)

try:
    print("=== Stage Pattern Test ===")
    stage_normal()
    stage_warning()
    stage_danger()

finally:
    pwm.stop()
    GPIO.cleanup()
    print("cleanup 완료")