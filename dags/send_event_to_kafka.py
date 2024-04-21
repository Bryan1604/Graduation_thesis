import datetime
from airflow import DAG 
from airflow.operators.python import PythonOperator
from kafka import KafkaConsumer, KafkaProducer

class KafkaConfig:
    def __init__(self, bootstrap_servers = 'localhost:9092', group_id = 'consumer-group', auto_offset_reset = 'earliest', topic = 'events'):
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.auto_offset_reset = auto_offset_reset
        self.topic = topic
    
kafkaConfig = KafkaConfig()

producer = KafkaProducer(bootstrap_servers= kafkaConfig.bootstrap_servers, max_block_ms=5000)
consumer = KafkaConsumer(kafkaConfig.topic, group_id=kafkaConfig.group_id, bootstrap_servers=kafkaConfig.bootstrap_servers)
# consumer.subscribe([topic])

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

# gui du leu vao kafka - sub thread
def send_to_kafka(demo_data):
    import json
    import time
    while True:  
            producer.send('events', json.dumps(demo_data).encode('utf-8'))
            producer.flush()
            time.sleep(1)

if __name__ == "__main__":
    demo_data = demo_data
    send_to_kafka(demo_data)
# with DAG('crawl_job_automation',
#          default_args=config.default_args,
#          schedule_interval=datetime.timedelta(hours=2),
#          catchup=False) as dag:
    
#     streaming_event = PythonOperator(
#         task_id = 'streaming_event_to_elasticsearch',
#         python_callable = send_to_kafka,
#         provide_context=True,
#     )
    
# [streaming_event]