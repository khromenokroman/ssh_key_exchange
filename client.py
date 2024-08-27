#!/usr/bin/python3
import socket
import argparse
import os
import sys


def save_public_key(user, key):
    """
    Saves the public key to the authorized_keys file in the user's .ssh directory.

    Parameters:
    user (str): The name of the user for whom the key will be saved.
    key (str): The public key to save.
    """
    try:
        os.makedirs(f'/root/.ssh', exist_ok=True)
        with open(f'/root/.ssh/authorized_keys', 'w') as file:
            file.write(key)
    except Exception as ex:
        print(f"Error: {ex}")
        sys.exit(-1)


def get_public_key(ip, port, user):
    """
    Connects to the server and retrieves the public key for the user.

    Parameters:
    ip (str): The IP address of the server.
    port (int): The port number on which the server is listening.
    user (str): The name of the user for whom the key will be retrieved.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))

        data = s.recv(1024).decode()

    print(f'Received public key for {user}:', repr(data))

    save_public_key(user, data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Receive public key from server.")
    parser.add_argument("user", help="username to save received public key")
    parser.add_argument("ip", help="IP address of the server")
    parser.add_argument("port", type=int, help="Port of the server")
    args = parser.parse_args()

    get_public_key(args.ip, args.port, args.user)
