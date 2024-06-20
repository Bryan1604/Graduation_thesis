import psutil
import socket  # Add this line

def get_ip_address(interface_name):
    for interface, addrs in psutil.net_if_addrs().items():
        if interface == interface_name:
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    return addr.address
    return None

if __name__ == "__main__":
    ip_address = get_ip_address("en0")
    if ip_address:
        print(f"Interface: en0, IP Address: {ip_address}")
    else:
        print("Interface not found or it does not have an IPv4 address.")