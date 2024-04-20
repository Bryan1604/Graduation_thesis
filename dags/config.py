from kafka import KafkaProducer,KafkaConsumer
from airflow.operators.python import PythonOperator
from elasticsearch import Elasticsearch
from datetime import datetime
# Kafka server configuration
bootstrap_servers = 'localhost:9092'
group_id = 'consumer-group'
auto_offset_reset = 'earliest'
topic = 'events'

# Default arguments
default_args = {
    'owner': 'airscholar',
    'start_date': datetime(2023, 12, 18, 10, 00)
}

producer = KafkaProducer(bootstrap_servers=bootstrap_servers, max_block_ms=5000)
consumer = KafkaConsumer(topic, group_id=group_id, bootstrap_servers=bootstrap_servers)
consumer.subscribe([topic])


es = Elasticsearch(['localhost:9200'])

demo_data = {
  "event_id": "123456",
  "time": "2022-03-15T08:00:00",
  "user_id": 123,
  "domain_userid": "user123",
  "event_type": "purchase",
  "products": [
    {
      "product_id": 1,
      "product_name": "Product 1",
      "price": 100,
      "quantity": 2,
      "category_id": 101
    },
    {
      "product_id": 2,
      "product_name": "Product 2",
      "price": 150,
      "quantity": 1,
      "category_id": 102
    }
  ]
}