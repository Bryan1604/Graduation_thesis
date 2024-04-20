import mysql.connector
import psycopg2

#noi chua db cua website
serverdb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    databse="CDP"
)

server_cursor = serverdb.cursor()

# Kết nối đến PostgreSQL ( noi chua customer data platform db)
cdpbd = psycopg2.connect(
  host="localhost",
  user="admin",
  password="admin",
  database="cdp"
)
postgres_cursor = cdpbd.cursor()

# Truy vấn dữ liệu từ MySQL
server_cursor.execute("SELECT * FROM customers ")
rows = server_cursor.fetchall()

# Insert dữ liệu vào PostgreSQL
for row in rows:
    postgres_cursor.execute("INSERT INTO customers VALUES (%s, %s, %s)", row)

# Commit và đóng kết nối
cdpbd.commit()
postgres_cursor.close()
cdpbd.close()

server_cursor.close()
serverdb.close()