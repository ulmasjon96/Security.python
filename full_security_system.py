import psutil
import time
import os
import hashlib
import subprocess

# Список подозрительных процессов
suspicious_processes = ['malware.exe', 'virus.exe', 'trojan.exe']
known_hashes = {
    'important_file.txt': '5d41402abc4b2a76b9719d911017c592',
}

def monitor_processes():
    print("Мониторинг процессов начат...")
    while True:
        processes = psutil.process_iter(['pid', 'name'])
        for process in processes:
            try:
                process_name = process.info['name']
                if process_name.lower() in suspicious_processes:
                    print(f"ОШИБКА: Найден подозрительный процесс: {process_name} (PID: {process.info['pid']})")
                    process.terminate()  # Завершаем процесс
                    print(f"Процесс {process_name} завершен.")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass  # Пропускаем процессы, к которым нет доступа
        time.sleep(10)

def get_file_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def check_file_integrity(directory, known_hashes):
    print("Проверка целостности файлов...")
    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            current_hash = get_file_hash(file_path)
            if file_name in known_hashes and known_hashes[file_name] != current_hash:
                print(f"Предупреждение! Изменен файл: {file_path}")

def block_ip(ip_address):
    try:
        os.system(f"sudo iptables -A INPUT -s {ip_address} -j DROP")  # Для Linux
        # Для Windows используйте netsh
        print(f"IP адрес {ip_address} заблокирован.")
    except Exception as e:
        print(f"Ошибка при блокировке IP: {e}")

def scan_file_with_clamav(file_path):
    result = subprocess.run(['clamscan', file_path], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    if "OK" in output:
        print(f"Файл {file_path} чист.")
    else:
        print(f"Файл {file_path} заражен!")

if __name__ == "__main__":
    # Запуск всех функций защиты
    monitor_processes()  # Мониторинг процессов
    check_file_integrity('C:/path/to/directory', known_hashes)  # Проверка целостности файлов
    block_ip('192.168.1.100')  # Блокировка подозрительного IP
    scan_file_with_clamav('C:/path/to/file')  # Сканирование файла на вирусы
