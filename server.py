#!/usr/bin/python3
import socket
import argparse
import os
import signal
import sys


def get_public_key(user):
    try:
        with open(f'/home/{user}/.ssh/id_rsa.pub', 'r') as file:
            public_key = file.read()
        return public_key
    except FileNotFoundError:
        return "Key not found"


def start_server(port, user):
    # Получение публичного ключа пользователя
    public_key = get_public_key(user)

    # Создание сокета
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen()
    print(f"Server started on port {port}")

    def signal_handler(sig, frame):
        print("\nServer is shutting down...")
        server.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    while True:
        # Ожидание подключения клиента
        client, addr = server.accept()
        with client:
            print(f"Connected by {addr}")
            # Отправка публичного ключа клиенту
            client.sendall(public_key.encode())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send public key by server.")
    parser.add_argument("user", help="username to find public key")
    args = parser.parse_args()

    start_server(1993, args.user)
