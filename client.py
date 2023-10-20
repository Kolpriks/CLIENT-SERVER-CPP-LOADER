import tkinter as tk
from tkinter import filedialog
import socket

host = '192.168.1.78'
port = 12345

def send_file(filename, host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        with open(filename, 'rb') as file:
            file_data = file.read()
            s.send(file_data)

def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        send_file(file_path, host, port)
        status_label.config(text="Файл успешно отправлен.")
        
        response_port = 12346  # Порт для ожидания ответа
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as response_socket:
            response_socket.bind(('0.0.0.0', response_port))
            response_socket.listen(1)
            status_label.config(text="Ожидаем ответ...")
            conn, addr = response_socket.accept()
            response_data = conn.recv(1024)
            if response_data is not None:
                status_label.config(text="Получен ответ: " + response_data.decode())
            else:
                status_label.config(text="Пусто!")

# Создание окна
root = tk.Tk()
root.title("Отправка файла")
root.geometry("600x300")  # Установка размера окна

# Создание метки и кнопки
label = tk.Label(root, text="Выберите файл для отправки:")
label.pack(pady=50)  # Увеличиваем отступ

browse_button = tk.Button(root, text="Обзор", command=browse_file)
browse_button.pack(pady=10)  # Увеличиваем отступ и размер кнопки

status_label = tk.Label(root, text="")
status_label.pack(pady=10)
status_label.config(font=("Helvetica", 12))  # Установка размера шрифта для текстовой метки

root.mainloop()
