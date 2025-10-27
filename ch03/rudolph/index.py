from flask import Flask, render_template
import RPi.GPIO as GPIO

app = Flask(__name__)

GPIO.setmode(GPIO.BOARD)

GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)   
GPIO.setup(10, GPIO.OUT, initial=GPIO.LOW)  
GPIO.setup(12, GPIO.OUT, initial=GPIO.LOW)  

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/onred")
def on_red():
    try:
        GPIO.output(8, GPIO.HIGH)
        return "ok"
    except:
        return "fail"

@app.route("/offred")
def off_red():
    try:
        GPIO.output(8, GPIO.LOW)
        return "ok"
    except:
        return "fail"

@app.route("/onyellow")
def on_yellow():
    try:
        GPIO.output(10, GPIO.HIGH)
        return "ok"
    except:
        return "fail"

@app.route("/offyellow")
def off_yellow():
    try:
        GPIO.output(10, GPIO.LOW)
        return "ok"
    except:
        return "fail"

@app.route("/ongreen")
def on_green():
    try:
        GPIO.output(12, GPIO.HIGH)
        return "ok"
    except:
        return "fail"

@app.route("/offgreen")
def off_green():
    try:
        GPIO.output(12, GPIO.LOW)
        return "ok"
    except:
        return "fail"

if __name__ == "__main__":
    app.run(host="0.0.0.0")