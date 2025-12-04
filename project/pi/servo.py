import RPi.GPIO as GPIO
from time import sleep

# BCM 기준 GPIO 번호
SERVO_PIN_1 = 5    # 서보1 (정방향)
SERVO_PIN_2 = 6    # 서보2 (역방향)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(SERVO_PIN_1, GPIO.OUT)
GPIO.setup(SERVO_PIN_2, GPIO.OUT)

servo1 = GPIO.PWM(SERVO_PIN_1, 50)   # 50Hz
servo2 = GPIO.PWM(SERVO_PIN_2, 50)   # 50Hz


def angle_to_duty(angle):
    """서보 각도 → duty 변환"""
    return 2.5 + (angle / 18)


def move_opposite(angle):
    """
    servo1은 angle로
    servo2는 반대 방향(180 - angle)로 이동
    """
    duty1 = angle_to_duty(angle)
    duty2 = angle_to_duty(180 - angle)   # 반대 방향

    print(f"[SERVO1] angle={angle}° / duty={duty1:.2f}")
    print(f"[SERVO2] angle={180 - angle}° (opposite) / duty={duty2:.2f}")

    servo1.ChangeDutyCycle(duty1)
    servo2.ChangeDutyCycle(duty2)

    sleep(0.5)

    # 떨림 방지
    servo1.ChangeDutyCycle(0)
    servo2.ChangeDutyCycle(0)


if __name__ == "__main__":
    try:
        servo1.start(0)
        servo2.start(0)

        print("== 동시 반대방향 테스트 ==")
        # 0도 → 90도 → 0도
        move_opposite(0)
        sleep(1)

        move_opposite(90)
        sleep(1)

        move_opposite(0)
        sleep(1)

    finally:
        servo1.stop()
        servo2.stop()
        GPIO.cleanup()
        print("GPIO cleanup 완료")