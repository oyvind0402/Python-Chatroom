import socket
import sys
import threading
import time

import requests

BASE = "http://127.0.0.1:5000/api/"

print("true")

def active_connection(username):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = "127.0.0.2"
    port = 5001
    try:
        client.connect((ip, port))
        client.send(username.encode())
    except:
        print("couldnt connect")
    # message = client.recv(1025)
    # print(message.decode())
    # message = client.recv(1025)
    # print(message.decode())
    # message = client.recv(1025)
    # print(message.decode())
    # client.send(username.encode())

    # client.send(username.encode())
    # print("message send")
    # time.sleep(2)
    # print("done sleeping")
    # data = client.recv(1024)
    # print(data.decode())




def print_response(response):
    try:
        print(response.json())
    except requests.exceptions.Timeout:
        print("Request timed out")
    except:
        print("Invalid request.")


def add_user(username):
    print("USER POST")
    response = requests.post(BASE + "user/" + str(username))
    print_response(response)
    if str(username) == response.json():
        connection = threading.Thread(target=active_connection(str(str(username))))
        connection.start()

    print("-------------------------------------------------------")


def get_user(username=None):
    if username == None or username == "":
        print("USER GET ALL")
        response = requests.get(BASE + "users")
    else:
        print("USER GET")
        response = requests.get(BASE + "user/" + str(username))
    print_response(response)
    print("-------------------------------------------------------")


def add_room(id):
    print("ROOM POST")
    response = requests.put(BASE + "room/" + str(id))
    print_response(response)
    print("-------------------------------------------------------")


def get_room(id=None):
    if id == None:
        print("ROOM GET ALL")
        response = requests.get(BASE + "rooms")
    else:
        print("ROOM GET")
        response = requests.get(BASE + "room/" + str(id))
    print_response(response)
    print("-------------------------------------------------------")


def add_roomuser(room_id, username):
    print("ROOMUSER PUT")
    response = requests.put(BASE + "room/" + str(room_id) + "/user/" + str(username))
    print_response(response)
    print("-------------------------------------------------------")


def get_roomuser(room_id, username=None):
    if username == None:
        print("ROOMUSER GET ALL")
        response = requests.get(BASE + "room/" + str(room_id) + "/users")
    else:
        print("ROOMUSER GET")
        response = requests.get(BASE + "room/" + str(room_id) + "/user/" + str(username))
    print_response(response)
    print("-------------------------------------------------------")


def add_message(room_id, username, message):
    print("MESSAGE PUT")
    response = requests.put(BASE + "room/" + str(room_id) + "/user/" + str(username) + "/message/" + str(message))
    print_response(response)
    print("-------------------------------------------------------")


def get_messages(room_id, username):
    print("MESSAGE GET")
    response = requests.get(BASE + "room/" + str(room_id) + "/user/" + str(username) + "/messages")
    print_response(response)
    print("-------------------------------------------------------")


print("--------------------------USER TESTS-----------------------------")
add_user("oyvind91")
add_user("oyvind91")
add_user("someone")
add_user(10)
get_user()



get_user("someone")
get_user("not_member")
get_user(1)
get_user(True)
get_user("      ")
get_user("")
get_user()

print("--------------------------ROOM TESTS-----------------------------")
add_room(0)
add_room(1)
add_room(1)
add_room("error")

get_room(0)
get_room(1)
get_room(2)
get_room("error")
get_room()

print("--------------------------ROOMUSER TESTS-----------------------------")
add_roomuser(0, "oyvind91")
add_roomuser(0, "someone")
add_roomuser("0", "oyvind91")
add_roomuser(1, "oyvind91")
add_roomuser("1", "error")
add_roomuser(1, "")
add_roomuser(2, "oyvind91")
add_roomuser("error", "oyvind91")

get_roomuser(0, "oyvind91")
get_roomuser(1, 10)
get_roomuser(0)
get_roomuser(1)
get_roomuser("error")
get_roomuser(1, "error")
get_roomuser("error", "oyvind91")

print("--------------------------MESSAGE TESTS-----------------------------")
add_message(0, "oyvind91", "hey")
add_message(0, "not_member", "hey")
add_message("error", "oyvind91", "hey")
add_message("error", "oyvind91", "")

get_messages(0, "oyvind91")
get_messages(1, "oyvind91")
get_messages(0, "error")
get_messages("error", "error")