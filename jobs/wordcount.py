from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType
from pyspark.streaming import StreamingContext
import os

KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "192.168.12.104:29092")
KAFKA_TOPIC_TEST = os.environ.get("KAFKA_TOPIC_TEST", "enriched")
KAFKA_API_VERSION = os.environ.get("KAFKA_API_VERSION", "7.3.1")

def main():
    spark = SparkSession.builder.appName("StreamingEvent")\
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,spark-streaming-kafka-0-10_2.12:3.5.0")\
        .getOrCreate()
    
    spark.sparkContext.setLogLevel('WARN')
    
    schema_event = StructType([
        StructField("event_id", StringType(), True),
        StructField("time", StringType(), True),
        StructField("user_id", IntegerType(), True),
        StructField("user_name", StringType(), True),
        StructField("phone_number", StringType(), True),
        StructField("email", StringType(), True), 
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
    
    # def read_kafka_topic(topic):
    #     return (spark.readStream
    #         .format('kafka')
    #         .option('kafka.bootstrap.servers', 'localhost:29092')
    #         .option('subscribe', topic)
    #         .option('startingOffsets', 'earliest')
    #         .load()
    #         .writeStream
    #         .format('console')
    #         .option('truncate', False)
    #         .start()
    #         )
        
    # read_kafka_topic('enriched')
            
    # Read data stream from Kafka
    kafka_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "192.168.12.104:29092") \
        .option("subscribe", KAFKA_TOPIC_TEST) \
        .option("startingOffsets", 'earliest') \
        .load()

    # Print the data to the console (without schema knowledge)
    kafka_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
        .writeStream \
        .format("console") \
        .start() \
        .awaitTermination()


    # Stop the SparkSession (optional)
    spark.stop()

if __name__ == "__main__":
    main()