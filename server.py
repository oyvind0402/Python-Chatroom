import socket
import sys
import threading
from timeit import Timer

list_connections = []
IP = "127.0.0.2"
port = 5001

push_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
push_socket.bind((IP, port))
push_socket.listen()

print("Server is live")

def placeholder():
    pass

def listening(client):
    message = "A connection has been made"
    print(message)
    username = client.recv(1024).decode()
    print(username + " received")
    for current_connection in list_connections:
        if current_connection["connection"] == client:
            current_connection["username"] = username
            print(current_connection)
    # if username == "api":
    #     while True:
    #         message = client.recv(1024)
    #         print(message.decode())
    # else:
    #     # a client so we need to notify
    #     client.close()
    print("yes")
    while True:
        do = "somethin"

    # username = push_socket.recv(1024).decode()
    # print(username)


while True:
    connection, address = push_socket.accept()
    list_connections.append({"connection": connection, "username": ""})
    new_client = threading.Thread(target=listening(connection))
    new_client.start()


def active_connection(client):
    username = client.recv().decode()
    for connection in list_connections:
        if connection == client:
            connection["username"] = username
            client.send(connection.encode())
