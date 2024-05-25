from pyspark.sql import SparkSession
from elasticsearch import Elasticsearch
import json

# Elasticsearch configuration
es = Elasticsearch(["http://elasticsearch:9200"])
INDEX_NAME = "streaming_event"

def create_es_index():
    if not es.indices.exists(index=INDEX_NAME):
        index_setting = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 1
            },
            "mappings": {
                "properties": {
                    "event_id": {"type": "keyword"},
                    "time": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss.SSS"},
                    "user_id": {"type": "keyword"},
                    "user_name": {"type": "keyword"},
                    "phone_number": {"type": "keyword"},
                    "email": {"type": "keyword"},
                    "event_type": {"type": "keyword"},
                    "domain_userid": {"type": "keyword"},
                    "products": {
                        "type": "nested",
                        "properties": {
                            "product_id": {"type": "keyword"},
                            "product_name": {"type": "keyword"},
                            "price": {"type": "keyword"},
                            "quantity": {"type": "keyword"},
                            "category": {"type": "keyword"}
                        }
                    }
                }
            }
        }
        try:
            es.indices.create(index=INDEX_NAME, body=index_setting)
            print(f"Index {INDEX_NAME} created successfully")
        except Exception as e:
            print(f"Failed to create index {INDEX_NAME}: {e}")
    else:
        return

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
                    "quantity": product_info.get("quantity") if product_info.get("quantity") is not None else 1
                }
            }

            # if event_data['event_type'] == "view":
            #     process_product_view(event_data['user_id'], event_data['products']['product_id'])

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
