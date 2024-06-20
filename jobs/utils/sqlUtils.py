import mysql.connector
import psutil
import socket  # Add this line

def get_ip_address(interface_name):
    for interface, addrs in psutil.net_if_addrs().items():
        if interface == interface_name:
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    return addr.address
    return None

# Thiết lập thông tin kết nối
config_server_db = {
    'host': 'localhost',            
    'user': 'root',                
    'password': '12345678',         
    'database': 'CDP',              
}

# Thiết lập thông tin kết nối toi cdp database
config_cdp_db = {
    'host': '192.168.10.134',     
    'user': 'root',                
    'password': '12345678',   
    'database': 'CDP_DB',    
}