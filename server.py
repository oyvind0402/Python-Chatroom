import socket
import sys
import threading
import time
from timeit import Timer

import requests

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
            print(current_connection["username"] + " is connected")
    while True:
        time.sleep(15)
        hi = "hei"
        client.send(hi.encode())



def new_messages():
    while True:
        base = "http://127.0.0.1:5000/api/"
        room = "rooms"
        response = requests.get(base + room)
        print(response.json())
        time.sleep(10)


def listen_connections():
    while True:
        print("code runs")
        connection, address = push_socket.accept()
        list_connections.append({"connection": connection, "username": ""})
        new_client = threading.Thread(target=listening(connection))
        new_client.start()


listen_for_new_messages = threading.Thread(target=listen_connections)
listen_for_new_messages.start()

while True:
    base = "http://127.0.0.1:5000/api/"
    room = "rooms"
    response = requests.get(base + room)
    print(response.json())
    time.sleep(10)
