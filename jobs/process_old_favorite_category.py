from pyspark.sql import SparkSession, DataFrame
from datetime import datetime, timedelta
from pyspark.sql.functions import reduce, col, expr
import mysql.connector
import json
from jobs.segments.combile import combile_operator
from jobs.utils.sqlUtils import config_cdp_db

if __name__ == "__main__":
    
    # connect to mysql cdp_db
    cdp_db = mysql.connector.connect(**config_cdp_db)
    cdp_cursor = cdp_db.cursor()
    
    three_days_ago = datetime.now() - timedelta(days=3)
    three_days_ago_str = three_days_ago.strftime('%Y-%m-%d %H:%M:%S')
    if cdp_db.is_connected():
        try:
            cdp_cursor.execute("DELETE FROM customer_category WHERE updated_at < %s ", (three_days_ago_str,))
            print("Update customer_category successfull")
            cdp_db.commit()
        except mysql.connector.Error as err:
            print("Error:", err)
            cdp_db.rollback()
        finally:
            # Đóng kết nối
            if 'cdp_db' in locals() and cdp_db.is_connected():
                cdp_db.close()
                print('Connection server closed')