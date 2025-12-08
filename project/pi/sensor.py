import RPi.GPIO as GPIO
import time
import requests

SENSOR_BOTTOM_PIN = 5
SENSOR_TOP_PIN    = 6

SERVO_PIN_1 = 20
SERVO_PIN_2 = 21

BUZZER_PIN = 26

RED_PIN   = 23
GREEN_PIN = 24
BLUE_PIN  = 25

BACKEND_BASE_URL = "http://10.150.2.4:8000"
SENSOR_ID = 1
LED_COLORS = {
    "normal": "#00FF00",
    "warning": "#FFA500",
    "danger": "#FF0000",
}
LED_REFRESH_INTERVAL = 0.5  # seconds

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

GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

red_pwm   = GPIO.PWM(RED_PIN, 500)
green_pwm = GPIO.PWM(GREEN_PIN, 500)
blue_pwm  = GPIO.PWM(BLUE_PIN, 500)

red_pwm.start(0)
green_pwm.start(0)
blue_pwm.start(0)


def angle_to_duty(angle):
    return 2.5 + (angle / 18)


def move_opposite(angle):
    duty1 = angle_to_duty(angle)
    duty2 = angle_to_duty(180 - angle)

    servo1.ChangeDutyCycle(duty1)
    servo2.ChangeDutyCycle(duty2)
    time.sleep(0.5)

    servo1.ChangeDutyCycle(0)
    servo2.ChangeDutyCycle(0)


def open_windows():
    move_opposite(90)
    print("[SERVO] 창문 열림")


def close_windows():
    move_opposite(0)
    print("[SERVO] 창문 닫힘")


def beep(freq, duration):
    buzzer_pwm.ChangeFrequency(freq)
    buzzer_pwm.start(50)
    time.sleep(duration)
    buzzer_pwm.stop()


def stage_warning_beep():
    for _ in range(3):
        beep(2000, 0.2)
        time.sleep(0.2)


def stage_danger_beep():
    # 일반적인 고조되는 경보음 톤(2kHz/2.5kHz) - 패턴은 유지
    beep(1000, 1.0)
    time.sleep(1)


def fetch_led_colors():
    global LED_COLORS
    try:
        res = requests.get(f"{BACKEND_BASE_URL}/api/led/colors", timeout=1.0)
        res.raise_for_status()
        data = res.json()
        LED_COLORS = {item["state"]: item["color_hex"] for item in data}
        print("[API] led colors updated:", LED_COLORS)
    except Exception as e:
        print("[API] fetch_led_colors error:", e)


def hex_to_duty(color_hex: str):
    color_hex = color_hex.lstrip("#")
    r = int(color_hex[0:2], 16) / 255
    g = int(color_hex[2:4], 16) / 255
    b = int(color_hex[4:6], 16) / 255
    return r, g, b


def set_led_color(r_norm, g_norm, b_norm):
    # Scale to 0-100 for common-cathode LED (1.0 = fully on)
    r = max(0, min(100, r_norm * 100))
    g = max(0, min(100, g_norm * 100))
    b = max(0, min(100, b_norm * 100))
    red_pwm.ChangeDutyCycle(r)
    green_pwm.ChangeDutyCycle(g)
    blue_pwm.ChangeDutyCycle(b)


def apply_led_state(state: str):
    color_hex = LED_COLORS.get(state, "#00FF00")
    r, g, b = hex_to_duty(color_hex)
    set_led_color(r, g, b)


def led_green():
    apply_led_state("normal")


def led_orange():
    apply_led_state("warning")


def led_red():
    apply_led_state("danger")


def led_off():
    set_led_color(0, 0, 0)


def apply_led_for_stage(stage):
    if stage >= 3:
        led_red()
    elif stage == 2:
        led_orange()
    else:
        led_green()


def send_stage_log(stage):
    url = f"{BACKEND_BASE_URL}/api/sensor/logs"
    payload = {
        "sensor_id": SENSOR_ID,
        "value": float(stage),
        "stage": int(stage),
    }
    try:
        res = requests.post(url, json=payload, timeout=1.0)
        print("[API] send_stage_log:", res.status_code, res.json())
    except Exception as e:
        print("[API] send_stage_log error:", e)


if __name__ == "__main__":
    servo1.start(0)
    servo2.start(0)
    close_windows()
    led_green()

    warning_done = False
    danger_done = False
    both_wet_start = None
    windows_open = False
    current_stage = 0
    fetch_led_colors()
    apply_led_for_stage(current_stage)
    last_led_refresh = time.time()

    send_stage_log(current_stage)

    try:
        print("=== Flood Control Loop Start ===")

        while True:
            bottom_raw = GPIO.input(SENSOR_BOTTOM_PIN)
            top_raw    = GPIO.input(SENSOR_TOP_PIN)

            bottom_wet = (bottom_raw == GPIO.HIGH)
            top_wet    = (top_raw   == GPIO.HIGH)

            new_stage = current_stage

            if not bottom_wet and not top_wet:
                both_wet_start = None
                warning_done = False
                danger_done = False
                led_green()
                if windows_open:
                    close_windows()
                    windows_open = False
                new_stage = 0

            elif bottom_wet and not top_wet:
                led_orange()
                new_stage = 2
                if not warning_done:
                    stage_warning_beep()
                    warning_done = True
                both_wet_start = None
                if windows_open:
                    close_windows()
                    windows_open = False

            elif bottom_wet and top_wet:
                if both_wet_start is None:
                    both_wet_start = time.time()

                elapsed = time.time() - both_wet_start

                if elapsed < 5.0 and not danger_done:
                    led_orange()
                    new_stage = 2

                if elapsed >= 5.0 and not danger_done:
                    open_windows()
                    windows_open = True
                    stage_danger_beep()
                    danger_done = True
                    new_stage = 3

                if danger_done:
                    new_stage = 3
                    led_red()

            if time.time() - last_led_refresh > LED_REFRESH_INTERVAL:
                fetch_led_colors()
                apply_led_for_stage(current_stage)
                last_led_refresh = time.time()

            if new_stage != current_stage:
                current_stage = new_stage
                send_stage_log(current_stage)
                apply_led_for_stage(current_stage)

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("종료합니다.")

    finally:
        close_windows()
        led_off()

        servo1.stop()
        servo2.stop()
        buzzer_pwm.stop()
        red_pwm.stop()
        green_pwm.stop()
        blue_pwm.stop()
        GPIO.cleanup()
        print("GPIO cleanup 완료")
