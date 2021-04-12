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


# def add_user(username):
#     print("USER POST")
#     response = requests.post(BASE + "user/" + str(username))
#     print_response(response)
#     if str(username) == response.json():
#         connection = threading.Thread(target=active_connection(str(str(username))))
#         connection.start()

#     print("-------------------------------------------------------")

def add_user(username):
    #print("USER POST")
    response = requests.post(BASE + "user/" + username)
    #print_response(response)
    return response

def get_all_users(querier):
    #print("USER GET ALL")
    response = requests.get(BASE + "users", {"username": querier})
    #print_response(response)
    return response

def get_user(username, querier):
    #print("USER GET")
    response = requests.get(BASE + "user/" + username, {"username": querier})
    #print_response(response)
    return response

def delete_user(username, querier):
    response = requests.delete(BASE + "user/" + username, data={"username": querier})
    return response


def add_room(room, roomname, querier):
    #print("ROOM POST")
    response = requests.post(BASE + "room/" + str(room), {"roomname": roomname, "username": querier})
    #print_response(response)
    return response

def get_all_rooms(querier):
    #print("ROOM GET ALL")
    response = requests.get(BASE + "rooms", {"username": querier})
    #print_response(response)
    return response

def get_room(room, querier):
    #print("ROOM GET")
    response = requests.get(BASE + "room/" + str(room), {"username": querier})
    #print_response(response)
    return response

def add_roomuser(room, username, querier):
    #print("ROOMUSER PUT")
    response = requests.put(BASE + "room/" + str(room) + "/user/" + username, {"username": querier})
    #print_response(response)
    return response

def get_all_roomusers(room, querier):
    #print("ROOMUSER GET ALL")
    response = requests.get(BASE + "room/" + str(room) + "/users", {"username": querier})
    #print_response(response)
    return response

def get_roomuser(room, username, querier):
    #print("ROOMUSER GET")
    response = requests.get(BASE + "room/" + str(room) + "/user/" + username, {"username": querier})
    #print_response(response)
    return response

def delete_roomuser(room, username, querier):
    #print("ROOMUSER DELETE")
    response = requests.delete(BASE + "room/" + str(room) + "/user/" + username, data={"username": querier})
    #print_response(response)
    return response

def add_message(room, username, message, querier):
    #print("MESSAGE PUT")
    response = requests.put(BASE + "room/" + str(room) + "/user/" + username + "/messages", {"username": querier, "message": message})
    #print_response(response)
    return response

def get_messages(room, querier):
    #print("MESSAGE GET")
    response = requests.get(BASE + "room/" + str(room) + "/messages", {"username": querier}) 
    #print_response(response)
    return response

def get_all_messages(room, username, querier):
    #print("MESSAGE GET ALL")
    response = requests.get(BASE + "room/" + str(room) + "/user/" + username + "/messages", {"username": querier})
    #print_response(response)
    return response

print("--------------------------USER TESTS-----------------------------")
# add_user("oyvind91")
# add_user("oyvind91")
# add_user("someone")
# add_user(10)
# get_user()



# get_user("someone")
# get_user("not_member")
# get_user(1)
# get_user(True)
# get_user("      ")
# get_user("")
# get_user()

print("--------------------------ROOM TESTS-----------------------------")
# add_room(0)
# add_room(1)
# add_room(1)
# add_room("error")

# get_room(0)
# get_room(1)
# get_room(2)
# get_room("error")
# get_room()

print("--------------------------ROOMUSER TESTS-----------------------------")
# add_roomuser(0, "oyvind91")
# add_roomuser(0, "someone")
# add_roomuser("0", "oyvind91")
# add_roomuser(1, "oyvind91")
# add_roomuser("1", "error")
# add_roomuser(1, "")
# add_roomuser(2, "oyvind91")
# add_roomuser("error", "oyvind91")

# get_roomuser(0, "oyvind91")
# get_roomuser(1, 10)
# get_roomuser(0)
# get_roomuser(1)
# get_roomuser("error")
# get_roomuser(1, "error")
# get_roomuser("error", "oyvind91")

print("--------------------------MESSAGE TESTS-----------------------------")
# add_message(0, "oyvind91", "hey")
# add_message(0, "not_member", "hey")
# add_message("error", "oyvind91", "hey")
# add_message("error", "oyvind91", "")

# get_messages(0, "oyvind91")
# get_messages(1, "oyvind91")
# get_messages(0, "error")
# get_messages("error", "error")