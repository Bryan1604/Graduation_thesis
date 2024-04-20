from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType
from pyspark.streaming import StreamingContext

# class KafkaManager:
#     def __init__(self, bootstrapServers, group_id, auto_offset_reset, topic):
#         self.bootstrapServers = bootstrapServers
#         self.group_id = group_id
#         self.auto_offset_reset = auto_offset_reset
#         self.topic = topic

# class SparkManager:
#     def __init__(self, app_name):
#         self.app_name = app_name
    
#     def create_spark_session(app_name):
#         return SparkSession.builder \
#             .appName(app_name) \
#             .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
#             .getOrCreate()
    
#     def read_from_kafka(spark, bootstrap_servers, topic):
#         return spark \
#             .readStream \
#             .format("kafka") \
#             .option("kafka.bootstrap.servers",bootstrap_servers) \
#             .option("subscribe", topic) \
#             .load()
    
#     def write_to_elasticsearch(sourceDF, elasticsearch_host, elasticsearch_port, checkpoint_location):
#         sourceDF.writeStream \
#         .format("org.elasticsearch.spark.sql") \
#         .option("es.nodes", elasticsearch_host) \
#         .option("es.port", elasticsearch_port) \
#         .option("checkpointLocation", checkpoint_location) \
#         .start("index_name/") \
#         .awaitTermination()
        

# khởi tạo 1 chương trình ảo đầy dữ liệu từ kafka vào elasticsearch để demo

# Định nghĩa checkpoint location
checkpoint_location = "/tmp/checkpoint_location"

# khởi tạo 1 phiên spark session
def create_spark_session(app_name):
    return  SparkSession.builder \
                .appName(app_name) \
                .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
                .getOrCreate()

# đọc dữ liệu từ kafka , tra ve dataframe
def read_from_kafka(spark, bootstrap_servers, topic):
    schema_event = StructType([
        StructField("event_id", StringType(), True),
        StructField("time", StringType(), True),
        StructField("user_id", IntegerType(), True),
        StructField("domain_userid", StringType(), True),
        StructField("event_type", StringType(), True),
        StructField("products", ArrayType(
            StructType([
                StructField("product_id", IntegerType(), True),
                StructField("product_name", StringType(), True),
                StructField("price", IntegerType(), True),
                StructField("quantity", IntegerType(), True),
                StructField("category_id", IntegerType(), True)
            ])
        ), True)
    ])
    
    # Đọc dữ liệu từ Kafka và chuyển đổi thành DataFrame
    kafka_df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", bootstrap_servers) \
        .option("subscribe", topic) \
        .load()
        
    # Chuyển đổi dữ liệu theo schema đã định nghĩa
    transformed_df = transform_data(kafka_df, schema_event)
    return transformed_df

# chuyển đổi dữ liệu theo schema
def transform_data(data, schema):
    return data.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*")    

# ghi trưc tiếp vào elastic search
def write_to_elasticsearch(sourceDF, elasticsearch_host, elasticsearch_port, checkpoint_location, index_name):
    sourceDF.writeStream \
    .format("org.elasticsearch.spark.sql") \
    .option("es.nodes", elasticsearch_host) \
    .option("es.port", elasticsearch_port) \
    .option("checkpointLocation", checkpoint_location) \
    .start(index_name) \
    .awaitTermination()

def main():
    spark_session = create_spark_session("event_treaming")
    
    # Tạo một Streaming Context với batch interval là 5 giây
    scc = StreamingContext(spark_session.sparkContext, 5)

    # Đặt cấu hình Kafka
    kafka_param = {
        "bootstrap.servers": "localhost:9092",
        "auto.offset.reset" : "latest",
        "group_id" : "consumer-group",
        "topic": "events"
    }

    # Đọc dữ liệu từ Kafka
    transformed_data = read_from_kafka(spark_session,"localhost:9092", "events")
    transformed_data.write \
        .format("org.elasticsearch.spark.sql") \
        .option("es.nodes", "your_elasticsearch_host") \
        .option("es.port", "9200") \
        .option("es.resource", "your_index_name/your_document_type") \
        .option("es.mapping.id", "event_id") \
        .save()
        
    # ghi vao elastic search
    write_to_elasticsearch(
        sourceDF=transformed_data,  # DataFrame chứa dữ liệu cần ghi
        elasticsearch_host="localhost",  # Địa chỉ host của Elasticsearch
        elasticsearch_port="9200",  # Cổng Elasticsearch
        checkpoint_location=checkpoint_location,  # Vị trí checkpoint
        index_name="events"  # Tên index mà bạn muốn ghi dữ liệu vào
    )


if __name__ == "__main__":
    main()
