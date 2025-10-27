from flask import Flask, request, render_template, jsonify
import db_model
import sensor_dht

app = Flask(__name__)

@app.route('/')
def home():
  return render_template("index.html")

@app.route('/now')
def insert_db():
  hum, temp = sensor_dht.get_now()
  result = db_model.insert(hum, temp)
  return result

@app.route('/record')
def select():
  result = db_model.select_all()
  return jsonify(result)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port="31337")