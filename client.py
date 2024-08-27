import socket


def get_public_key(ip, port):
    # Создание сокета
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))

        # Получение данных (публичного ключа) от сервера
        data = s.recv(1024)

    print('Received', repr(data))


# Замените 'localhost' на IP-адрес сервера, если он запущен на другой машине
get_public_key('localhost', 1993)