import socket

# Замените это на ваш публичный ключ
public_key = """-----BEGIN PUBLIC KEY-----
...Your public key here...
-----END PUBLIC KEY-----"""


def start_server(port):
    # Создание сокета
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(('0.0.0.0', port))
        server.listen()
        print(f"Server started on port {port}")

        while True:
            # Ожидание подключения клиента
            client, addr = server.accept()
            with client:
                print(f"Connected by {addr}")
                # Отправка публичного ключа клиенту
                client.sendall(public_key.encode())


start_server(1993)
