import adafruit_dht
import board

def get_now():
  sensor = adafruit_dht.DHT11(board.D14)
  temp = sensor.temperature
  hum = sensor.humidity
  return [hum, temp]