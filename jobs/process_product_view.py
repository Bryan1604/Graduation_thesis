import os
import json
import re
import mysql.connector
from elasticsearch import Elasticsearch
from utils.sqlUtils import config_cdp_db, config_server_db
from kafka import KafkaConsumer, TopicPartition

# connect to mysql cdp_db
cdp_db = mysql.connector.connect(**config_cdp_db)
cdp_cursor = cdp_db.cursor()

def process_product_view(user_id, product_id):
    if cdp_db.is_connected():
        try:
            cdp_cursor.execute("INSERT INTO customer_product (customer_id, product_id, view_count) VALUES (%s, %s, 1) ON DUPLICATE KEY UPDATE view_count = view_count + 1", (user_id, product_id))
            cdp_db.commit()
            print("Successfully updated view_count.")
        except mysql.connector.Error as err:
            print("Error:", err)
            cdp_db.rollback()

            