import os
import platform

def block_ip(ip_address):
    try:
        system = platform.system()
        
        if system == 'Linux':
            os.system(f"sudo iptables -A INPUT -s {ip_address} -j DROP")
            print(f"IP адрес {ip_address} заблокирован на Linux.")
        elif system == 'Windows':
            os.system(f"netsh advfirewall firewall add rule name=\"Block IP {ip_address}\" dir=in action=block remoteip={ip_address}")
            print(f"IP адрес {ip_address} заблокирован на Windows.")
        else:
            print("Неизвестная операционная система. Блокировка не поддерживается.")
    except Exception as e:
        print(f"Ошибка при блокировке IP: {e}")

# Пример блокировки IP
block_ip('192.168.1.100')
