import psutil
import time
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Настройка логирования
logging.basicConfig(filename='process_monitor.log', level=logging.INFO)

suspicious_processes = ['malware.exe', 'virus.exe', 'trojan.exe']

# Отправка уведомления по электронной почте
def send_email_alert(process_name):
    try:
        sender_email = "your_email@example.com"
        receiver_email = "receiver_email@example.com"
        password = "your_password"
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = 'Предупреждение: Подозрительный процесс найден'

        body = f"Найден подозрительный процесс: {process_name}. Рекомендуется проверить его."
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP_SSL('smtp.example.com', 465) as server:
            server.login(sender_email, password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
        logging.info(f"Уведомление отправлено: {process_name}")
    except Exception as e:
        logging.error(f"Ошибка при отправке уведомления: {e}")

def monitor_processes():
    print("Мониторинг процессов начат...")
    while True:
        processes = psutil.process_iter(['pid', 'name'])
        for process in processes:
            try:
                process_name = process.info['name']
                if process_name.lower() in suspicious_processes:
                    print(f"ОШИБКА: Найден подозрительный процесс: {process_name} (PID: {process.info['pid']})")
                    logging.info(f"Найден подозрительный процесс: {process_name} (PID: {process.info['pid']})")
                    process.terminate()  # Завершаем процесс
                    logging.info(f"Процесс {process_name} завершен.")
                    send_email_alert(process_name)  # Отправка уведомления
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        time.sleep(10)
