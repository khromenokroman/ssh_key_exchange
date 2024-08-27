#!/usr/bin/python3
import socket
import argparse
import os


def save_public_key(user, key):
    # Создание .ssh директории в случае отсутствия
    if user != 'root':
        os.makedirs(f'/home/{user}/.ssh', exist_ok=True)
        with open(f'/home/{user}/.ssh/authorized_keys', 'w') as file:
            file.write(key)
    else:
        os.makedirs(f'/root/.ssh', exist_ok=True)
        with open(f'/root/.ssh/authorized_keys', 'w') as file:
            file.write(key)


def get_public_key(ip, port, user):
    # Создание сокета
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))

        # Получение данных (публичного ключа) от сервера
        data = s.recv(1024).decode()

    print(f'Received public key for {user}:', repr(data))

    # Сохранение полученного публичного ключа
    save_public_key(user, data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Receive public key from server.")
    parser.add_argument("user", help="username to save received public key")
    parser.add_argument("ip", help="IP address of the server")
    parser.add_argument("port", type=int, help="Port of the server")
    args = parser.parse_args()

    get_public_key(args.ip, args.port, args.user)
