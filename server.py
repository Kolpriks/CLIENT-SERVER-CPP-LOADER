import socket
import subprocess
import os

def receive_file(filename, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', port))
        s.listen(1)
        print("Ждем подключения...")
        conn, addr = s.accept()
        print(f"Подключено с {addr[0]}:{addr[1]}")

        with open(filename, 'wb') as file:
            file_data = conn.recv(1024)
            while file_data:
                file.write(file_data)
                file_data = conn.recv(1024)

        return addr  # Возвращаем адрес клиента
    
def send_result(result, host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.send(result)
        return 0 

def compile_and_run_cpp(file_path):
    try:
        # Получаем имя файла без расширения
        base_filename = os.path.splitext(os.path.basename(file_path))[0]

        # Компилируем файл в исполняемый файл
        compile_command = f"g++ {file_path} -o {base_filename}"
        compile_process = subprocess.Popen(compile_command, shell=True)
        compile_process.wait()

        if compile_process.returncode == 0:
            # Если компиляция прошла успешно, запускаем программу
            run_command = f"./{base_filename}"
            run_process = subprocess.Popen(run_command, shell=True, stdout=subprocess.PIPE)
            run_process.wait()

            if run_process.returncode == 0:
                print("Программа успешно выполнена.")
                output = run_process.stdout.read()
                return output  # Возвращаем результат выполнения программы
            else:
                print("Ошибка выполнения программы.")
        else:
            print("Ошибка компиляции.")
            return None

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        return None



if __name__ == "__main__":
    port = 12345
    received_file_path = '/home/kolpriks/Documents/All/Study/Ky/6_practice/TEST.cpp'
    sender_address = receive_file(received_file_path, port)

    result = compile_and_run_cpp(received_file_path)
    
    if result is not None:
        send_result(result, sender_address[0], 12346)
    else:
        res='Error! Nekorektnaya Kompilyatciya'
        send_result(res, sender_address[0], 12346)