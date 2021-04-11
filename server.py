import socket
import sys

list_connections = []
IP = "127.0.0.2"
port = 5001

push_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
push_socket.bind((IP, port))
push_socket.listen()

print("connected")

while True:
    connection_test, address = push_socket.accept()
    list_connections.append(connection_test)
    message = "connected"
    print(message)
    connection_test.send(message.encode())


def active_connection(client):
    username = client.recv().decode()
    for connection in list_connections:
        if connection == client:
            connection["username"] = username
            client.send(connection.encode())
