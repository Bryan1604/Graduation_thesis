import sys
import os
from pyspark.sql import SparkSession
from segment_type import SegmentField, Operator, DataType
from datetime import datetime
import mysql.connector

spark = SparkSession.builder.appName('ProcessSegment')\
    .config('spark.jars.packages', 'com.mysql:mysql-connector-j:8.4.0') \
    .getOrCreate()

sqlContext = SparkSession(spark)
spark.sparkContext.setLogLevel("ERROR")

# Database connection properties
db_url = 'jdbc:mysql://192.168.12.104:3306/CDP_DB'
db_properties = {
    'driver': 'com.mysql.cj.jdbc.Driver',
    'user': 'root',
    'password': '12345678'
}

# Thiết lập thông tin kết nối toi cdp database
config_cdp_db = {
    'host': '192.168.12.104',           
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
    update_time = datetime.now()
    for customer in customers.collect():
        cdp_cursor.execute("INSERT INTO customer_segment (customer_id, segment_id, update_time) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE customer_id = VALUES(customer_id), segment_id = VALUES(segment_id)", (customer['customer_id'], segmentId,update_time ))
    cdp_db.commit()
    print("Successfully updated customer_segment")

#loc ra nhung khach hang co dieu kien thoa man phan khuc , lay 1 thong tin ve phan khuc
#segmentsInfo la danh sach cac segment trong dastabase
def filterCustomer(customerdf, segmentdf) :
    #xu ly
    for segment in segmentdf.collect():
        condition = segment['rule']
        # customers = customerdf.filter((customerdf[condition['field']] > condition['value']))
        customers = customerdf.filter((customerdf['total_purchase'] < 8))
        customers.show()
        segmentId = segment['segment_id']
        
        #update vao database bang customer_segment
        updateSegmentCustomer(customers, segmentId)
    
# xoa du lieu cu khi duoc cap nhat
def deleteSegmentCustomer():
    return

if __name__ == "__main__":
    #vi du ve 1 dieu kien cua segment
    segmentInfo = {
            'field' : SegmentField.TOTAL_PRODUCT_VIEW,
            'operator' : Operator.GREATER_THAN,
            'type': DataType.INTEGER,
            'value': 18
    }
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