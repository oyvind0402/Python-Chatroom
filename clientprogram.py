import requests
import time
import sys
import random


print("----------------------------------------------")
print("Welcome to the electric boogaloo API chatroom!")
print("----------------------------------------------")


BASE = "http://127.0.0.1:5000/api/"


while True:
    username = input("Type in your username:")
    response = requests.post(BASE + "user/" + username)
    if response.status_code == 201:
        print("User created with username: " + username)
        break
    elif response.status_code == 409:
        print("A user already exists with that username, try another name.")
        continue


print("Thanks for joining the server! Type --help for a list of commands.")


while True:
    message = input(f'{username}: ')
    if message == '--help':
        print("Type --create to create create a chat room, type --help to show this help prompt, type --showrooms 
        "to show all rooms, type --join to join a chatroom, type --showmessages to show all messages for a specific chatroom, type --showmymessages to show all your messages for a specific chatroom.")
    elif message == '--create':
        while True:
            roomname = input("Type in the roomname: ")
            roomid = hash(roomname)
            response = requests.post(BASE + "room/" + str(roomid))
            if response.status_code == 201:
                print("Chat room called " + roomname + " created.")
                joinmessage = input("Do you wish to join the room you just created?")
                if joinmessage == 'Y' or joinmessage == 'y' or joinmessage == 'yes' or joinmessage == 'Yes' or joinmessage == 'YES':
                    response = requests.put(BASE + "room/" + roomid + "/user/" + username)
                    print("Joined " + roomname)
                    break
                elif joinmessage == 'N' or joinmessage == 'n' or joinmessage == 'no' or joinmessage == 'No' or joinmessage == 'NO':
                    break
            elif response.status_code == 409:
                print("A room already exists with that roomname, try again.")
                continue
    elif message == '--showrooms':
        response = requests.get(BASE + "rooms")
        print("Rooms:")
        print(response.json())
    elif message == '--join':
        roommsg = input("If you want to see a list of rooms to join type '--show'")
        if roommsg == '--show':
            response = requests.get(BASE + "rooms")
            print("Rooms:")
            print(response.json())
        else:
            print("You decided not to show rooms.")
            roomchoice = input("Type the room_id of the room you wish to join: ")
            # Need to make sure the input is a number
            response = requests.put(BASE + "room/" + roomchoice + "/user/" + username)
