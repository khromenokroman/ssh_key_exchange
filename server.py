#!/usr/bin/python3
import socket
import argparse
import signal
import sys


def get_public_key(user):
    """
    Fetches the public key of the provided user.

    Parameters:
    user (str): The name of the user.

    Returns:
    str: The public key of the user if found, else a message stating "Key not found".
    """
    try:
        with open(f'/home/{user}/.ssh/id_rsa.pub', 'r') as file:
            public_key = file.read()
        return public_key
    except Exception as ex:
        print(f"Error: {ex}")
        sys.exit(-1)


def start_server(port, user):
    """
    Starts a server at the provided port and listens for incoming connections.
    On receiving a connection, sends the public key of the user to the client.

    Parameters:
    port (int): The port number at which the server should run.
    user (str): The name of the user whose public key should be sent.
    """
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
        client, addr = server.accept()
        with client:
            print(f"Connected by {addr}")
            client.sendall(public_key.encode())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send public key by server.")
    parser.add_argument("user", help="username to find public key")
    args = parser.parse_args()

    start_server(1993, args.user)
