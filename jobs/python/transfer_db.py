import mysql.connector
from utils.sqlUtils import config_cdp_db, config_server_db
# Kết nối đến cơ sở dữ liệu
try:
    server_db = mysql.connector.connect(**config_server_db)
    cdp_db = mysql.connector.connect(**config_cdp_db)
    
    # Kiểm tra kết nối thành công
    if server_db.is_connected() and cdp_db.is_connected():
        print('Connected to MySQL database')
        server_cursor = server_db.cursor()
        cdp_cursor = cdp_db.cursor()
       
        # transfer  customer data
        server_cursor.execute("SELECT * FROM customers ")
        rows = server_cursor.fetchall()
        for row in rows:
            cdp_cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (row[0],))
            record = cdp_cursor.fetchone()
            if record:
                cdp_cursor.execute("UPDATE customers SET fullname = %s, email = %s, phone_number = %s WHERE customer_id = %s", (row[1], row[2], row[3], row[0]))
            else :
                cdp_cursor.execute("INSERT INTO customers (customer_id, fullname, email, phone_number) VALUES (%s, %s, %s, %s)", (row[0],row[1], row[2], row[3]))
                print("Inserted data for customer ID:", row[0])
        cdp_db.commit()
        
         #transfer category data 
        server_cursor.execute("SELECT * FROM categories ")
        rows = server_cursor.fetchall()
        for row in rows :
            cdp_cursor.execute("INSERT INTO categories (category_id, category_name, imagecategoryUrl) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE category_name = VALUES(category_name), imagecategoryUrl = VALUES(imagecategoryUrl)", (row[0], row[1], row[2]))
        cdp_db.commit()
        
        #transfer products data
        server_cursor.execute("SELECT * FROM products ")
        rows = server_cursor.fetchall()
        for row in rows:
            cdp_cursor.execute("SELECT * FROM products WHERE product_id = %s", (row[0],))
            record = cdp_cursor.fetchone()
            #TODO: thiếu trường update_time
            if record:
                cdp_cursor.execute("UPDATE products SET product_name = %s, description = %s, price = %s , category_id = %s, image_url = %s  WHERE product_id = %s", (row[1], row[2], row[3], row[4], row[5], row[0]))
            else :
                cdp_cursor.execute("INSERT INTO products (product_id, product_name, description , price, category_id, image_url) VALUES (%s, %s, %s, %s, %s, %s)", (row[0],row[1], row[2], row[3], row[4], row[5]))
                print("Inserted data for product ID:", row[0])
        cdp_db.commit()
        
       
        
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    # Đóng kết nối
    if 'server_db' in locals() and server_db.is_connected():
        server_db.close()
        print('Connection server closed')

    if 'cdp_db' in locals() and cdp_db.is_connected():
        cdp_db.close()
        print('Connection cdp closed')


# # Truy vấn dữ liệu từ MySQL
# server_cursor.execute("SELECT * FROM customers ")


# rows = server_cursor.fetchall()
# for row in server_cursor:
#     print(row)





