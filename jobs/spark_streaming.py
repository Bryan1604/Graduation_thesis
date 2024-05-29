from pyspark.sql import SparkSession
from elasticsearch import Elasticsearch
from pyspark.sql.functions import col,from_json, udf, when
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType
from utils.sqlUtils import config_cdp_db
from utils.esUtils import es, create_es_index, INDEX_NAME
import json

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


# # Hàm trích xuất dữ liệu người dùng từ JSON
# def get_user_info(json_str):
#     try:
#         json_obj = json.loads(json_str)
#         if len(json_obj["data"]) > 2:
#             user_info = json_obj["data"][2]["data"]
#             return json.dumps(user_info)
#     except Exception as e:
#         return json.dumps({})
#     return json.dumps({})

# # Hàm trích xuất dữ liệu sự kiện từ JSON
# def get_event_info(json_str):
#     try:
#         json_obj = json.loads(json_str)
#         event_info = json_obj["data"]["data"]
#         return json.dumps(event_info)
#     except Exception as e:
#         return json.dumps({})
#     return json.dumps({})

# # Hàm trích xuất thông tin sản phẩm từ JSON
# def get_product_info(json_str):
#     try:
#         json_obj = json.loads(json_str)
#         product_info = json_obj["data"][0]["data"]
#         return json.dumps(product_info)
#     except Exception as e:
#         return json.dumps({})
#     return json.dumps({})

# def get_json_strings(data):
#     jsonStrings = find_json_strings(data)
#     return jsonStrings

# def process_batch(df, batch_id) :
#     # Áp dụng các UDF để xử lý và tạo các cột mới
#     df = df.withColumn("user_info_json", get_user_info(get_json_strings(col("value"))[0]))
#     df = df.withColumn("event_info_json", get_event_info(get_json_strings(col("value"))[1]))
#     df = df.withColumn("product_info_json", get_product_info(get_json_strings(col("value"))[0]))

#     df = df.withColumn("user_id", col("user_info_json").getItem("user_id"))
#     df = df.withColumn("user_name", col("user_info_json").getItem("user_name"))
#     df = df.withColumn("phone_number", col("user_info_json").getItem("phone_number"))
#     df = df.withColumn("email", col("user_info_json").getItem("email"))

#     df = df.withColumn("event_type", col("event_info_json").getItem("action"))

#     df = df.withColumn("product_id", col("product_info_json").getItem("id"))
#     df = df.withColumn("product_name", col("product_info_json").getItem("name"))
#     df = df.withColumn("price", col("product_info_json").getItem("price"))
#     df = df.withColumn("quantity", col("product_info_json").getItem("quantity").cast(IntegerType()))
#     df = df.withColumn("quantity", when(col("quantity").isNull(), 1).otherwise(col("quantity")))
#     df.show()
def process_batch(df, batch_id):
    events = df.collect()
    for row in events:
        data = row["value"]
        split_data = data.split('\t')
        clean_data = [item.strip() for item in split_data if item]
        
        jsonStrings = find_json_strings(data)

        user_info = json.loads(jsonStrings[0])["data"][2]["data"] if len(jsonStrings) > 0 and len(json.loads(jsonStrings[0])["data"]) > 2 else {}
        event_info = json.loads(jsonStrings[1])["data"]["data"]
        product_info = json.loads(jsonStrings[0])["data"][0]["data"]

        if len(jsonStrings) > 1 and user_info.get("user_id") is not None:
            event_data = {
                "event_id": clean_data[6],
                "time": clean_data[2],
                "user_id": user_info.get("user_id"),
                "user_name": user_info.get("user_name"),
                "phone_number": user_info.get("phone_number"),
                "email": user_info.get("email"),
                "event_type": event_info["action"],
                "domain_userid": clean_data[12] if user_info.get("user_id") is None else clean_data[13],
                "products": {
                    "product_id": product_info["id"],
                    "product_name": product_info["name"],
                    "price": product_info["price"],
                    "quantity": product_info.get("quantity") if product_info.get("quantity") is not None else 1,
                    "category": product_info["category"],
                }
            }
            print(event_data)
            try:
                es.index(index=INDEX_NAME, body=event_data)
                print(f"document indexed successfully")
            except Exception as e:
                print(f"Failed to index document: {e}")
            es.indices.refresh(index=INDEX_NAME)

if __name__ == "__main__":
    #connect to elasticsearch
    create_es_index()
    # Tạo Spark session
    spark = SparkSession.builder \
        .appName("StreamingEvent") \
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
