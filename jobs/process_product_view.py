from utils.sqlUtils import config_cdp_db
from pyspark.sql import SparkSession
import json
import mysql.connector

# connect to mysql cdp_db
cdp_db = mysql.connector.connect(**config_cdp_db)
cdp_cursor = cdp_db.cursor()

def process_product_view(user_id, product_id):
    if cdp_db.is_connected():
        try:
            cdp_cursor.execute("INSERT INTO customer_product (customer_id, product_id, view_count) VALUES (%s, %s, 1) ON DUPLICATE KEY UPDATE view_count = view_count + 1", (user_id, product_id))
            cdp_db.commit()
            print("Successfully updated view_count.")
        except mysql.connector.Error as err:
            print("Error:", err)
            cdp_db.rollback()

def find_json_strings(data):
        json_strings = []
        start = data.find('{')
        while start != -1:
            counter = 1
            end = start + 1
            while counter > 0 and end < len(data):
                if data[end] == '{':
                    counter += 1
                elif data[end] == '}':
                    counter -= 1
                end += 1
            if counter == 0:
                json_strings.append(data[start:end])
            start = data.find('{', end)
        return json_strings

def process_batch(df, batch_id):
    events = df.collect()
    for row in events:
        data = row["value"]
        jsonStrings = find_json_strings(data)
        user_info = json.loads(jsonStrings[0])["data"][2]["data"] if len(jsonStrings) > 0 and len(json.loads(jsonStrings[0])["data"]) > 2 else {}
        event_info = json.loads(jsonStrings[1])["data"]["data"]
        product_info = json.loads(jsonStrings[0])["data"][0]["data"]

        if len(jsonStrings) > 1 and user_info.get("user_id") is not None:
            user_id = user_info.get("user_id")
            product_id = product_info["id"]
            if event_info["action"] == "view":
                process_product_view(user_id, product_id)
            
if __name__ == "__main__":

    # Tạo Spark session
    spark = SparkSession.builder \
        .appName("Process_Product_View") \
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

            