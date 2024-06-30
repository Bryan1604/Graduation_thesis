# Lay ra nhung the loai ma nguoi dung quan tam gan day ( so thich ngan han )
from pyspark.sql import SparkSession
import mysql.connector
from utils.sqlUtils import config_cdp_db
from extensions.json_extension import find_json_strings
import json

# connect to mysql cdp_db
cdp_db = mysql.connector.connect(**config_cdp_db)
cdp_cursor = cdp_db.cursor()

def check_exist_customer_category(customer_id, category_id) :
    rows = cdp_cursor.execute("select * from customer_category where customer_id = %s and category_id = %s", (customer_id, category_id))
    rows = cdp_cursor.fetchall()
    if len(rows) > 0 :
        return True
    return False
       
        
def update_customer_category(customer_id, category):
    if cdp_db.is_connected():
        try:
            cdp_cursor.execute("SELECT category_id FROM categories WHERE category_name = %s LIMIT 1", (category,))
            category_id_row = cdp_cursor.fetchone()
            if category_id_row:
                category_id = category_id_row[0]
                if check_exist_customer_category(customer_id, category_id):
                    cdp_cursor.execute("UPDATE customer_category SET updated_at= CURRENT_TIMESTAMP WHERE customer_id = %s AND category_id = %s ", ( customer_id, category_id))
                else :
                    cdp_cursor.execute("INSERT INTO customer_category (customer_id, category_id) VALUES (%s, %s) ", (customer_id, category_id))
                #cdp_cursor.execute("INSERT INTO customer_category (customer_id, category_id) VALUES (%s, (select category_id from categories where category_name = %s limit 1)) ON DUPLICATE KEY UPDATE category_id = VALUES(category_id), customer_id = VALUES(customer_id) ", (user_id, category))
                cdp_db.commit()
            print("Successfully updated customer_category.")
        except mysql.connector.Error as err:
            print("Error:", err)
            cdp_db.rollback()
            
def process_event(data):
    jsonStrings = find_json_strings(data)
    user_info = json.loads(jsonStrings[0])["data"][2]["data"] if len(jsonStrings) > 0 and len(json.loads(jsonStrings[0])["data"]) > 2 else {}
    event_info = json.loads(jsonStrings[1])["data"]["data"]
    product_info = json.loads(jsonStrings[0])["data"][0]["data"]

    if len(jsonStrings) > 1 and user_info.get("user_id") is not None and event_info["action"] != "purchase":
        user_id = user_info.get("user_id")
        category = product_info["category"]
        print(product_info)
        update_customer_category(user_id, category)

def process_batch(df, batch_id):
    events = df.collect()
    for row in events:
        process_event(row["value"])
            
if __name__ == "__main__":

    # Tạo Spark session
    spark = SparkSession.builder \
        .appName("Process_Favorite_Category") \
        .getOrCreate()
    
    # Chỉ log ra canh bao
    spark.sparkContext.setLogLevel("WARN")
    
    # Đọc dữ liệu từ Kafka
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka1:9092") \
        .option("subscribe", "enriched") \
        .load()

    # Chuyển đổi dữ liệu từ Kafka thành chuỗi
    df = df.selectExpr("CAST(value AS STRING)")
    # In dữ liệu ra console
    query = df.writeStream \
        .outputMode("update") \
        .format("console") \
        .foreachBatch(process_batch) \
        .start()

    query.awaitTermination()

            