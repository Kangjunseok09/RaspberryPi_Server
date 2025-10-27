import pymysql

conn = pymysql.connect(host='localhost', user='root', password='q1w2e3', db='study_db')
cur = conn.cursor()

def add_angle(angle):
  cur.execute("insert into record_angle(angle) values('{}')".format(angle))
  conn.commit()