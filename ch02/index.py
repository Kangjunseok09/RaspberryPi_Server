from flask import Flask, render_template, redirect, url_for, request
import pymysql
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/<int:count>")
def send(count):
    print(count)
    return redirect(url_for("home"))

@app.route("/send", methods=["POST"])
def save_db():
    data = request.get_json()
    value = data.get("value")
    print(value)  # 터미널 확인용

    conn = pymysql.connect(host="localhost", user="root", passwd="q1w2e3", db="study")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO numcount (num) VALUES (%s)", (value,))
    conn.commit()

    cursor.close()
    conn.close()


    return redirect(url_for("home"))

@app.route("/send/<int:num>")
def up(num):
    conn = pymysql.connect(host='localhost', user='root', passwd='q1w2e3', db='study')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO numcount (num) VALUES (%s)", (num,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=31337)