import subprocess
import threading
import logging

# Настройка логирования
logging.basicConfig(filename='virus_scan.log', level=logging.INFO)

# Функция для сканирования файла с использованием ClamAV
def scan_file_with_clamav(file_path):
    try:
        result = subprocess.run(['clamscan', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        if "OK" in output:
            logging.info(f"Файл {file_path} чист.")
            print(f"Файл {file_path} чист.")
        else:
            logging.warning(f"Файл {file_path} заражен!")
            print(f"Файл {file_path} заражен!")
    except Exception as e:
        logging.error(f"Ошибка при сканировании файла {file_path}: {e}")

def scan_multiple_files(file_paths):
    threads = []
    for file_path in file_paths:
        thread = threading.Thread(target=scan_file_with_clamav, args=(file_path,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# Пример сканирования нескольких файлов
scan_multiple_files(['file1.txt', 'file2.exe', 'file3.zip'])
