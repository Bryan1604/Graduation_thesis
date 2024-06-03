import mysql.connector
# import psutil

# def get_ip_address(interface_name):
#     addrs = psutil.net_if_addrs()
#     if interface_name in addrs:
#         for addr in addrs[interface_name]:
#             if addr.family == psutil.AF_INET:
#                 return addr.address
#     return None

# Thiết lập thông tin kết nối
config_server_db = {
    'host': 'localhost',            
    'user': 'root',                
    'password': '12345678',         
    'database': 'CDP',              
}

# Thiết lập thông tin kết nối toi cdp database
config_cdp_db = {
    'host': '172.19.200.176',     
    'user': 'root',                
    'password': '12345678',   
    'database': 'CDP_DB',    
}