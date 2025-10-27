import pymysql

conn = pymysql.connect(host='localhost', user='root', password='q1w2e3', db='study_db')
cur = conn.cursor() #SQL 문을 실행하거나 실행된 결과를 돌려받는 통로

def add_status(status):
    cur.execute("insert into record_led(status) values('{0}')".format(status))
    conn.commit()


