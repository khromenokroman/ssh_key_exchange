#!/usr/bin/python3
import socket
import argparse
import os


def save_public_key(user, key):
    # Создание .ssh директории в случае отсутствия
    os.makedirs(f'/home/{user}/.ssh', exist_ok=True)
    with open(f'/home/{user}/.ssh/received_key.pub', 'w') as file:
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


def main():
    parser = argparse.ArgumentParser(description="Receive public key from server.")
    parser.add_argument("user", help="username to save received public key")
    args = parser.parse_args()

    # Замените 'localhost' на IP вашего сервера, если он запущен на другой машине
    get_public_key('localhost', 1993, args.user)


if __name__ == "__main__":
    main()
