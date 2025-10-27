from flask import Flask, request, render_template, jsonify
import RPi.GPIO as GPIO
import db_model
from time import sleep

app = Flask(__name__)

pin = 16

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)
servo = GPIO.PWM(pin, 50) # pin을 PWM 모드 50Hz로 사용
servo.start(0)

#서보모터는 주파수에 따라 동작하기 때문에
#사용자 편의를 위해 각도(angle)를 듀티사이클(duty)로 변환해 사용한다.
def setAngle(angle):
  duty = 2.5 + 10 * angle / 180
  print(f"degree : {angle} to {duty}(duty)")
  servo.ChangeDutyCycle(duty)

@app.route("/")
def home():
  return render_template("index.html")

@app.route('/angle', methods=['POST'])
def control_servo():
  data = request.get_json()
  angle = data.get('angle')
  if data is not None:
    setAngle(int(angle))
    db_model.add_angle(int(angle))
    return jsonify({"message": "OK"})

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=31337)
