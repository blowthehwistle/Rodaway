import sqlite3

# SQLite 데이터베이스 연결
conn = sqlite3.connect('flight_reservation.db')
cursor = conn.cursor()

# Passenger 테이블 생성 쿼리
create_table_query = '''
CREATE TABLE Passenger (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    english_name TEXT,
    baptism_name TEXT,
    grade TEXT,
    phone_number TEXT
);
'''

# 테이블 생성
cursor.execute(create_table_query)

# 변경사항 저장 및 연결 종료
conn.commit()
conn.close()
