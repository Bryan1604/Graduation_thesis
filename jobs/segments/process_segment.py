from pyspark.sql import SparkSession, DataFrame
from datetime import datetime
from pyspark.sql.functions import reduce, col, expr
import mysql.connector
import json
from jobs.segments.combile import combile_operator
from jobs.utils.sqlUtils import config_cdp_db

# Database connection properties
db_url = 'jdbc:mysql://192.168.10.134:3306/CDP_DB'
db_properties = {
    'driver': 'com.mysql.cj.jdbc.Driver',
    'user': 'root',
    'password': '12345678'
}

# Thiết lập thông tin kết nối toi cdp database
config_cdp_db = {
    'host': '192.168.10.134',           
    'user': 'root',                
    'password': '12345678',   
    'database': 'CDP_DB',    
}

# Load DataFrames from MySQL
def load_df(table_name):
    return spark.read \
        .format('jdbc') \
        .option('url', db_url) \
        .option('dbtable', table_name) \
        .options(**db_properties) \
        .load()

#update bang segment_customer
def updateSegmentCustomer(customers, segmentId) :
    for customer in customers.collect():
        cdp_cursor.execute("INSERT INTO customer_segment (customer_id, segment_id) VALUES (%s, %s) ON DUPLICATE KEY UPDATE customer_id = VALUES(customer_id), segment_id = VALUES(segment_id)", (customer['customer_id'], segmentId))
    cdp_cursor.execute("UPDATE segments SET updated_at= CURRENT_TIMESTAMP WHERE segment_id = %s", (segmentId,))
    cdp_db.commit()
    print("Successfully updated customer_segment")

#loc ra nhung khach hang co dieu kien thoa man phan khuc , lay 1 thong tin ve phan khuc
#segmentsInfo la danh sach cac segment trong dastabase
def filterCustomer(customerdf, segmentdf) :
    #xu ly
    for segment in segmentdf.collect():
        conditions_json = segment['rule']
        conditions = json.loads(conditions_json)
        filter_expresstion = " AND ".join([combile_operator(cond['condition'], cond['operator'],cond['type'], cond['value']) for cond in conditions])
        customers = customerdf.filter(expr(filter_expresstion))
        customers.show()
        updateSegmentCustomer(customers, segment['segment_id'])
    
# xoa du lieu cu khi duoc cap nhat
def deleteSegmentCustomer():
    return

if __name__ == "__main__":
    spark = SparkSession.builder.appName('ProcessSegment')\
        .config('spark.jars.packages', 'mysql:mysql-connector-java:8.0.28') \
        .getOrCreate()

    sqlContext = SparkSession(spark)
    spark.sparkContext.setLogLevel("ERROR")
    
    # connect to mysql cdp_db
    cdp_db = mysql.connector.connect(**config_cdp_db)
    cdp_cursor = cdp_db.cursor()

    customerdf = load_df('customers')
    segmentdf = load_df('segments')
    if cdp_db.is_connected():
        try:
            filterCustomer(customerdf, segmentdf)
        except mysql.connector.Error as err:
            print("Error:", err)
            cdp_db.rollback()
        finally:
            # Đóng kết nối
            if 'cdp_db' in locals() and cdp_db.is_connected():
                cdp_db.close()
                print('Connection server closed')