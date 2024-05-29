from elasticsearch import Elasticsearch

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