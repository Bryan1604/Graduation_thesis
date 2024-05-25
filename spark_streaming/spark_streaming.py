from pyspark.sql import SparkSession

# Tạo Spark session
spark = SparkSession.builder \
    .appName("StreamingEvent") \
    .getOrCreate()

# Đọc dữ liệu từ Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka1:9092") \
    .option("subscribe", "enriched") \
    .load()

# Chuyển đổi dữ liệu từ Kafka thành chuỗi
df = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# In dữ liệu ra console
query = df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
