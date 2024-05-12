from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType
from pyspark.streaming import StreamingContext


spark = SparkSession.builder \
        .appName("event_streaming") \
        .master("spark://spark-master:7077") \
        .config("spark.streaming.stopGracefullyOnShutdown", "true") \
        .getOrCreate()
    
data = [("Alice", 25)]
df = spark.createDataFrame(data, ["Name", "Age"])
df.show()
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:29092") \
    .option("subscribe", "enriched") \
    .load()    
            # .startingOffsets("earliest") \
            # .load()
            
kafka_df.printSchema()