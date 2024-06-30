# lay ra nhung san pham ma nguoi dung quan tam nhieu nhat
from pyspark.sql import SparkSession
import mysql.connector
from utils.sqlUtils import config_cdp_db
from utils.esUtils import es,INDEX_NAME
from datetime import datetime
from pyspark.sql.functions import col, count, desc, collect_list, udf, lit
from pyspark.sql.types import StringType

 
# Define a UDF to join strings with a separator
def join_strings(data, sep):
    return sep.join(map(str, data))  # Convert elements to strings

def get_all_document():
    scroll_size = 1000  # Số lượng tài liệu mỗi lần cuộn
    scroll_time = '1m'  # Thời gian giữ phiên cuộn

    response = es.search(
        index=INDEX_NAME,
        scroll=scroll_time,
        size=scroll_size,
        body={
            "query": {"match_all": {}}
        }
    )
    scroll_id = response['_scroll_id']
    hits = response['hits']['hits']
    all_hits = hits

    # Tiếp tục lấy các kết quả tiếp theo sử dụng scroll_id
    while len(hits) > 0:
        response = es.scroll(
            scroll_id=scroll_id,
            scroll=scroll_time
        )
        scroll_id = response['_scroll_id']
        hits = response['hits']['hits']
        all_hits.extend(hits)
    return all_hits

def get_latest_document():
    scroll_size = 1000  # Số lượng tài liệu mỗi lần cuộn
    scroll_time = '1m'  # Thời gian giữ phiên cuộn
    schedule_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    response = es.search(
        index=INDEX_NAME,
        scroll=scroll_time,
        size=scroll_size,
        body={
            "query": {
                "range": {
                    "time": {
                        "gte": schedule_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                    }
                }
            }
        }
    )
    scroll_id = response['_scroll_id']
    hits = response['hits']['hits']
    all_hits = hits

    # Tiếp tục lấy các kết quả tiếp theo sử dụng scroll_id
    while len(hits) > 0:
        response = es.scroll(
            scroll_id=scroll_id,
            scroll=scroll_time
        )
        scroll_id = response['_scroll_id']
        hits = response['hits']['hits']
        all_hits.extend(hits)
    return all_hits

if __name__ == "__main__":
    schedule_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    events = get_all_document()
    latest_events = get_latest_document()
    spark = SparkSession.builder \
        .appName("Process_Long_Hobbies") \
        .getOrCreate()
    try:
        cdp_db = mysql.connector.connect(**config_cdp_db)
        df_view = spark.read.json(spark.sparkContext.parallelize(events).map(lambda x: x['_source']))
        df_grouped = df_view.groupBy("user_id", "products").agg(count("*").alias("view_count"))
        top_products = df_grouped.orderBy(desc("view_count")).groupBy("user_id").agg(collect_list("products.product_id").alias("favorite_products"))
        top_products_list = top_products.collect()
        join_strings_udf = udf(join_strings, StringType())
        top_products = top_products.withColumn(
            "favorite_products_string",
            join_strings_udf(col("favorite_products"), lit(",")) 
        )
        if cdp_db.is_connected():
            cdp_cursor = cdp_db.cursor()
            for hit in latest_events:
                user_id = hit['_source']['user_id']
                cdp_cursor.execute("UPDATE customers SET favorite_products = %s WHERE customer_id = %s", (top_products.filter(col("user_id") == user_id).select("favorite_products_string").first()[0] ,user_id ))
        cdp_db.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'cdp_db' in locals() and cdp_db.is_connected():
            cdp_db.close()
            print('Connection server closed')
    spark.stop()
    
