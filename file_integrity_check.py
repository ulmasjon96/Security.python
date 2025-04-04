import hashlib
import os
import json
import logging

# Настройка логирования
logging.basicConfig(filename='file_integrity.log', level=logging.INFO)

# Загрузка хеш-сумм из файла
def load_known_hashes():
    with open('known_hashes.json', 'r') as file:
        return json.load(file)

# Функция для вычисления хеш-суммы
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
                logging.warning(f"Изменен файл: {file_path}")

# Пример загрузки хеш-сумм
known_hashes = load_known_hashes()

# Проверка целостности
check_file_integrity('C:/path/to/directory', known_hashes)
