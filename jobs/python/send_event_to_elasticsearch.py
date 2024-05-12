import os
import json
import re
import mysql.connector
from elasticsearch import Elasticsearch
from utils.sqlUtils import config_cdp_db, config_server_db
from kafka import KafkaConsumer, TopicPartition
from process_product_view import process_product_view

KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:29092")
KAFKA_TOPIC_TEST = os.environ.get("KAFKA_TOPIC_TEST", "enriched")
KAFKA_API_VERSION = os.environ.get("KAFKA_API_VERSION", "7.3.1")

# connect to mysql cdp_db
cdp_db = mysql.connector.connect(**config_cdp_db)
cdp_cursor = cdp_db.cursor()

# elastic search config
es = Elasticsearch(["http://localhost:9200"])
index_name = "streaming_event"
file_path = 'data.txt'

#Load last commited offset from a file
def load_offset():
    try: 
        with open('offset.txt', 'r') as file:
            offset_value = file.read().strip()
            return int(offset_value) if offset_value else None
    except FileNotFoundError:
        return None

#Save last commited offset to a file
def save_offset(offset):
    with open('offset.txt', 'w') as file:
        file.write(str(offset))
        
consumer = KafkaConsumer(
    KAFKA_TOPIC_TEST,
    bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
    api_version=KAFKA_API_VERSION,
    auto_offset_reset="earliest",
    # enable_auto_commit=True,
    enable_auto_commit=False,
)

# load last commited offset
last_offset = load_offset()
if last_offset is not None:
    for partition in consumer.partitions_for_topic(KAFKA_TOPIC_TEST):
        tp = TopicPartition(KAFKA_TOPIC_TEST, partition)
        consumer.seek(tp, last_offset)

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

def connect_elasticsearch():
    if not es.indices.exists(index=index_name):
        index_setting = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                "properties": {
                    "event_id": {"type": "keyword"},
                    "time": {
                        "type": "date",
                        "format": "yyyy-MM-dd HH:mm:ss.SSS"},
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
                            "quantity": {"type": "keyword", "ignore_malformed": True},
                            # "size": {"type": "keyword", "ignore_malformed": True},
                            "category": {"type": "keyword"},
                        }
                    }
                }
            }
        }
        try:
            es.indices.create(index=index_name, body=index_setting)
            print(f"Index {index_name} created successfully")
        except Exception as e:
            print(f"Failed to create index {index_name}: {e}")


# def update_total_view(user_id, product_id):
#     if cdp_db.is_connected():
#         try:
#             cdp_cursor.execute("INSERT INTO customer_product (customer_id, product_id, view_count) VALUES (%s, %s, 1) ON DUPLICATE KEY UPDATE view_count = view_count + 1", (user_id, product_id))
#             cdp_db.commit()
#             print("Successfully updated view_count.")
#         except mysql.connector.Error as err:
#             print("Error:", err)
#             cdp_db.rollback()

connect_elasticsearch()

while True:
        for message in consumer:
            # Lấy dữ liệu từ Kafka message
            data = message.value.decode("utf-8")
            # Parse dữ liệu thành JSON object
            print('---------------\n')
            split_data = data.split('\t')
            # Xóa kí tự xuống dòng và kí tự trắng từ cả hai phía của mỗi phần tử
            clean_data = [item.strip() for item in split_data]

            # Lọc ra các phần tử không rỗng
            clean_data = [item for item in clean_data if item]
            
            jsonStrings = find_json_strings(data)
            
            user_info = json.loads(jsonStrings[0])["data"][2]["data"] if len(jsonStrings) > 0 and len(json.loads(jsonStrings[0])["data"]) > 2 else {}
            event_info = json.loads(jsonStrings[1])["data"]["data"]
            product_info = json.loads(jsonStrings[0])["data"][0]["data"]
            
            if(len(jsonStrings) >1 and user_info.get("user_id") != None ):
                event_data = {
                    "event_id": clean_data[6],
                    "time": clean_data[2],
                    "user_id": user_info.get("user_id"),
                    "user_name": user_info.get("user_name"),
                    "phone_number": user_info.get("phone_number"),
                    "email": user_info.get("email"),
                    "event_type": event_info["action"],
                    "domain_userid": clean_data[12] if user_info.get("user_id") == None else clean_data[13] ,
                    "products" : {
                        "product_id" : product_info["id"],
                        "product_name" : product_info["name"],
                        "price" : product_info["price"],
                        "quantity" : product_info.get("quantity") if product_info.get("quantity") is not None else 1 ,
                        # "size" : product_info.get("size"),
                        "category": product_info["category"],
                    }
                }
                
                # update total of view 
                if(event_data['event_type'] == "view") :
                    process_product_view(event_data['user_id'], event_data['products']['product_id'])
                
                print(event_data)
                try:
                    es.index(index=index_name, body=event_data)
                    print(f"document indexed successfully")
                except Exception as e:
                    print(f"Failed to index document: {e}")
                es.indices.refresh(index=index_name)
                # json_file.write(json.dumps(event_data, indent=4))
                
            save_offset(message.offset)
            
  