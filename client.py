import socket
import sys
import threading
import time

import requests

BASE = "http://127.0.0.1:5000/api/"

def add_user(username):
    response = requests.post(BASE + "user/" + username)
    return response

def get_all_users(querier):
    response = requests.get(BASE + "users", {"username": querier})
    return response

def get_user(username, querier):
    response = requests.get(BASE + "user/" + username, {"username": querier})
    return response

def delete_user(username, querier):
    response = requests.delete(BASE + "user/" + username, data={"username": querier})
    return response

def add_room(room, roomname, querier):
    response = requests.post(BASE + "room/" + str(room), {"roomname": roomname, "username": querier})
    return response

def get_all_rooms(querier):
    response = requests.get(BASE + "rooms", {"username": querier})
    return response

def get_room(room, querier):
    response = requests.get(BASE + "room/" + str(room), {"username": querier})
    return response

def add_roomuser(room, username, querier):
    response = requests.put(BASE + "room/" + str(room) + "/user/" + username, {"username": querier})
    return response

def get_all_roomusers(room, querier):
    response = requests.get(BASE + "room/" + str(room) + "/users", {"username": querier})
    return response

def get_roomuser(room, username, querier):
    response = requests.get(BASE + "room/" + str(room) + "/user/" + username, {"username": querier})
    return response

def delete_roomuser(room, username, querier):
    response = requests.delete(BASE + "room/" + str(room) + "/user/" + username, data={"username": querier})
    return response

def add_message(room, username, message, querier):
    response = requests.put(BASE + "room/" + str(room) + "/user/" + username + "/messages", {"username": querier, "message": message})
    return response

def get_messages(room, username, querier):
    response = requests.get(BASE + "room/" + str(room) + "/user/" + username + "/messages", {"username": querier})
    return response

def get_all_messages(room, querier):
    response = requests.get(BASE + "room/" + str(room) + "/messages", {"username": querier}) 
    return response