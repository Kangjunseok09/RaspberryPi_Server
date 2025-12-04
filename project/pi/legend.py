import RPi.GPIO as GPIO
import time

SENSOR_BOTTOM_PIN = 23
SENSOR_TOP_PIN    = 14

SERVO_PIN_1 = 5
SERVO_PIN_2 = 6

BUZZER_PIN = 10

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(SENSOR_BOTTOM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SENSOR_TOP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(SERVO_PIN_1, GPIO.OUT)
GPIO.setup(SERVO_PIN_2, GPIO.OUT)

servo1 = GPIO.PWM(SERVO_PIN_1, 50)
servo2 = GPIO.PWM(SERVO_PIN_2, 50)

GPIO.setup(BUZZER_PIN, GPIO.OUT)
buzzer_pwm = GPIO.PWM(BUZZER_PIN, 1000)
buzzer_pwm.start(0)


def angle_to_duty(angle: float) -> float:
    return 2.5 + (angle / 18)


def move_opposite(angle: float):
    duty1 = angle_to_duty(angle)
    duty2 = angle_to_duty(180 - angle)

    print(f"[SERVO1] angle={angle}° / duty={duty1:.2f}")
    print(f"[SERVO2] angle={180 - angle}° / duty={duty2:.2f}")

    servo1.ChangeDutyCycle(duty1)
    servo2.ChangeDutyCycle(duty2)
    time.sleep(0.5)

    servo1.ChangeDutyCycle(0)
    servo2.ChangeDutyCycle(0)


def open_windows():
    print("[WINDOW] 창문 열기 (90도)")
    move_opposite(90)


def close_windows():
    print("[WINDOW] 창문 닫기 (0도)")
    move_opposite(0)


def beep(freq: int, duration: float):
    print(f"[BUZZER] beep freq={freq}, duration={duration}")
    buzzer_pwm.ChangeFrequency(freq)
    buzzer_pwm.start(50)
    time.sleep(duration)
    buzzer_pwm.stop()


def stage_warning_beep():
    print("[BUZZER] Stage 2 - Warning")
    for _ in range(3):
        beep(2000, 0.2)
        time.sleep(0.2)


def stage_danger_beep():
    print("[BUZZER] Stage 3 - Danger")
    beep(3000, 1.5)


if __name__ == "__main__":
    servo1.start(0)
    servo2.start(0)

    warning_done = False
    danger_done = False
    both_wet_start = None

    try:
        print("=== Flood Control Loop Start ===")

        while True:
            bottom_raw = GPIO.input(SENSOR_BOTTOM_PIN)
            top_raw    = GPIO.input(SENSOR_TOP_PIN)

            bottom_wet = (bottom_raw == GPIO.HIGH)
            top_wet    = (top_raw == GPIO.HIGH)

            print(
                f"[SENSORS] bottom={bottom_raw} ({'WET' if bottom_wet else 'DRY'}), "
                f"top={top_raw} ({'WET' if top_wet else 'DRY'}), "
                f"warning_done={warning_done}, danger_done={danger_done}"
            )

            if not bottom_wet and not top_wet:
                both_wet_start = None
                warning_done = False
                danger_done = False
                time.sleep(0.5)
                continue

            if bottom_wet and not top_wet:
                if not warning_done:
                    stage_warning_beep()
                    warning_done = True
                both_wet_start = None

            elif bottom_wet and top_wet:
                if both_wet_start is None:
                    both_wet_start = time.time()
                    print("[STATE] 두 센서 모두 WET 시작")

                elapsed = time.time() - both_wet_start
                if elapsed >= 5.0 and not danger_done:
                    print("[STATE] 5초 WET → 창문 열기 + 경고음")
                    open_windows()
                    stage_danger_beep()
                    danger_done = True

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("종료합니다.")

    finally:
        print("[WINDOW] 프로그램 종료 → 창문 0도로 복귀")
        close_windows()

        servo1.stop()
        servo2.stop()
        buzzer_pwm.stop()
        GPIO.cleanup()
        print("GPIO cleanup 완료")