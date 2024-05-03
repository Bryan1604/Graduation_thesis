import os
from kafka import KafkaConsumer
import json
import re
KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:29092")
KAFKA_TOPIC_TEST = os.environ.get("KAFKA_TOPIC_TEST", "enriched")
KAFKA_API_VERSION = os.environ.get("KAFKA_API_VERSION", "7.3.1")

consumer = KafkaConsumer(
    KAFKA_TOPIC_TEST,
    bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
    api_version=KAFKA_API_VERSION,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
)
# for message in consumer:
#     data = message
#     data = message.value.decode("utf-8")
#     data = json.dumps(data, indent=4)
#     print(str(data))


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

file_path = 'data.txt'

with open(file_path, "a") as json_file:
    for message in consumer:
        print('-----------')
        # Lấy dữ liệu từ Kafka message
        data = message.value.decode("utf-8")
        # Parse dữ liệu thành JSON object
        split_data = data.split('\t')

        # Trích xuất thông tin
        timestamp = split_data[2]
        user_email = split_data[10]
        # product_data = json.loads(split_data[-3])
        # action_data = json.loads(split_data[-2])

        # # Tạo các đối tượng JSON tương ứng
        # product_entity = product_data['data'][0]['data']
        # product_json = {
        #     "id": product_entity["id"],
        #     "name": product_entity["name"],
        #     "price": product_entity["price"],
        #     "currency": product_entity["currency"],
        #     "quantity": product_entity["quantity"],
        #     "category": product_entity["category"],
        #     "size": product_entity["size"]
        # }

        # user_context = product_data['data'][2]['data']
        # user_json = {
        #     "user_id": user_context["user_id"],
        #     "user_name": user_context["user_name"],
        #     "phone_number": user_context["phone_number"],
        #     "email": user_context["email"]
        # }

        # action_json = {
        #     "action": action_data['data']['data']['action']
        # }

        # # In các đối tượng JSON
        # print("Product JSON:")
        # print(json.dumps(product_json, indent=4))

        # print("\nUser JSON:")
        # print(json.dumps(user_json, indent=4))

        # print("\nAction JSON:")
        # print(json.dumps(action_json, indent=4))
        json_file.write( '---------------')
        # cleaned_data = [item for item in split_data if item.strip()]
        # for item in cleaned_data:
        #     json_file.write( item + '\n')

        jsonStrings = find_json_strings(data)
        for json_str in jsonStrings:
            json_obj = json.loads(json_str)
            print(json_obj)
            json_file.write(json.dumps(json_obj, indent=4))