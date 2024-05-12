from elasticsearch import Elasticsearch
from pyspark.sql import SparkSession
import mysql.connector
from utils.sqlUtils import config_cdp_db, config_server_db
from datetime import datetime
from pyspark.sql.functions import col, explode, split, count, desc, collect_list, concat_ws, expr, struct, udf, lit
from pyspark.sql.types import StringType


schedule_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
es = Elasticsearch(["http://localhost:9200"])
es_index = "streaming_event"
es_nodes = "localhost"
es_port = "9200"
es_resource = f"{es_index}"

events = es.search(index=es_index, body={"query" : {"match_all": {}}})
# Truy vấn Elasticsearch để lấy các sự kiện sau thời gian cụ thể
latest_events = es.search(index=es_index, body={"query": {"range": {"time": {"gte": schedule_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]}}}})

# Tạo một phiên Spark
spark = SparkSession.builder \
    .appName("ProcessHobbies") \
    .getOrCreate()
    
try:
    cdp_db = mysql.connector.connect(**config_cdp_db)
    
    # Chuyển kết quả từ Elasticsearch thành DataFrame và lọc ra các sự kiện "view"
    df_view = spark.read.json(spark.sparkContext.parallelize(events['hits']['hits']).map(lambda x: x['_source'])).filter(col("event_type") == "view")

    # Nhóm các sự kiện theo user_id và sản phẩm, đếm số lần xuất hiện của mỗi cặp
    df_grouped = df_view.groupBy("user_id", "products").agg(count("*").alias("view_count"))

    # Sắp xếp các cặp theo số lần xuất hiện giảm dần và thu thập danh sách sản phẩm theo user_id
    top_products = df_grouped.orderBy(desc("view_count")).groupBy("user_id").agg(collect_list("products.product_id").alias("top_products"))
    
    # Collect the DataFrame into a list of Python objects
    top_products_list = top_products.collect()
    
    # Define a UDF to join strings with a separator
    def join_strings(data, sep):
        return sep.join(map(str, data))  # Convert elements to strings

    join_strings_udf = udf(join_strings, StringType())  # Define UDF return type

    # Add a new column named 'top_products_string'
    top_products = top_products.withColumn(
        "top_products_string",
        join_strings_udf(col("top_products"), lit(",")) 
    )
    # Print the updated DataFrame
    top_products.show()

    if cdp_db.is_connected():
        cdp_cursor = cdp_db.cursor()
        #xu lys voi nhung user co hoat dong trong ngay
        for hit in latest_events['hits']['hits']:
            user_id = hit['_source']['user_id']
            update_time = datetime.strptime(hit['_source']['time'], '%Y-%m-%d %H:%M:%S.%f')
            cdp_cursor.execute("UPDATE customers SET favorite_products = %s , updated_time = %s WHERE customer_id = %s", (top_products.filter(col("user_id") == user_id).select("top_products_string").first()[0] , update_time,user_id ))
    cdp_db.commit()
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    # Đóng kết nối
    if 'cdp_db' in locals() and cdp_db.is_connected():
        cdp_db.close()
        print('Connection server closed')
spark.stop()