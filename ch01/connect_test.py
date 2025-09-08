import pymysql

#1. 연결
conn = pymysql.connect(host='localhost', user='kang', password='q1w2e3', db='shopping_db1')

#2. 커서
cur = conn.cursor()

#3. 쿼리 작성
cur.execute('select avg(age) from customer where address = "경기"')

#4. 결과값 조회
result = cur.fetchone()
print(int(result[0]))
#5. 종료(연결해제)
cur.close()
conn.close()


