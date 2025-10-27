import pymysql

conn = pymysql.connect(host='localhost', user='root', password='q1w2e3', db='study_db')
cur = conn.cursor()

def select_all():
  cur.execute("select * from record_dht")
  result = cur.fetchall()
  return result

def insert(hum, temp):
  cur.execute("insert into record_dht(humidity, temperature) values(%s, %s)", (hum, temp))
  conn.commit()
  return [hum, temp]
