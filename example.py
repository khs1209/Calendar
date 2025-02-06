import sqlite3

# SQLite 데이터베이스 연결
conn = sqlite3.connect('example.db')
print("Database created and connected!")

# 연결 종료
conn.close()
