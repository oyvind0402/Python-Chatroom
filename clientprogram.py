from threading import Timer

import requests
import time
import sys
import random


print("----------------------------------------------")
print("Welcome to the electric boogaloo API chatroom!")
print("----------------------------------------------")


BASE = "http://127.0.0.1:5000/api/"


while True:
    username = input("Type in your username: ")
    response = requests.post(BASE + "user/" + username)
    if response.status_code == 201:
        print("User created with username: " + username)
        break
    elif response.status_code == 409:
        print("A user already exists with that username, try another name.")
        continue


print("Thanks for joining the server! Type --help for a list of commands.")

def def_pass():
    pass

def chatroom(room_id):
    in_room = True
    message_input = ""

    while in_room:
        print(f"you are now in the room: {room_id}")
        print("Feel free to type whatever you would like")
        timeout = 5.0
        timer_thread = Timer(timeout, def_pass)
        timer_thread.start()
        try:
            message_input = input(username + ":")
        except EOFError:
            print("you have chosen to end the problem and that is your loss")
            sys.exit()
        timer_thread.cancel()
        print("timer cancelled")

        if message_input.__contains__("exit"):
            break
        response = requests.put(BASE + "room/" + str(room_id) + "/user/" + username + "/message/" + message_input)
        print(response.json())
        response = requests.get(BASE + "room/" + str(room_id) + "/user/" + username + "/messages")
        print(response.json())




while True:
    message = input(f'{username}: ')
    if message == '--help':
        print("Type '--create' to create a chat room\nType '--help' to show this help prompt\nType '--showrooms' " + 
        "to show all rooms\nType '--start' to join a chatroom to start typing messages\nType '--join' to join a chatroom\n" +
        "Type '--showmessages' to show all messages for a specific chatroom\nType '--showmymessages' to show all your messages for a specific chatroom.")
    elif message == '--create':
        while True:
            roomname = input("Type in the roomname: ")
            roomid = (hash(roomname) % 256)
            response = requests.put(BASE + "room/" + str(roomid), {"roomname": roomname})
            if response.status_code == 201:
                print("Chat room called " + roomname + " created.")
                joinmessage = input("Do you wish to join the room you just created?: ")
                if joinmessage == 'Y' or joinmessage == 'y' or joinmessage == 'yes' or joinmessage == 'Yes' or joinmessage == 'YES':
                    response = requests.put(BASE + "room/" + str(roomid) + "/user/" + username)
                    print("Joined " + roomname)
                    chatroom(roomid)
                    break
                elif joinmessage == 'N' or joinmessage == 'n' or joinmessage == 'no' or joinmessage == 'No' or joinmessage == 'NO':
                    break
            elif response.status_code == 409:
                print("A room already exists with that roomname, try again.")
                continue
            elif response.status_code == 404:
                print("Wrong syntax for the roomname")
    elif message == '--showrooms':
        response = requests.get(BASE + "rooms")
        print("Rooms:")
        print(response.json())
    elif message == '--join':
        roommsg = input("If you want to see a list of rooms to join type '--show': ")
        if roommsg == '--show':
            response = requests.get(BASE + "rooms")
            print("Rooms:")
            print(response.json())
        else:
            print("You decided not to show rooms.")
        roomchoice = input("Type the room_id of the room you wish to join: ")
        response = requests.put(BASE + "room/" + roomchoice + "/user/" + username)
        if response.status_code == 201:
            print(username + " successfully joined room " + roomchoice)
            chatroom(roomchoice)
        elif response.status_code == 404:
            print("Couldnt join room " + roomchoice + ". No room with that ID.")
        else:
            print("Something went wrong joining room " + roomchoice)
    elif message == '--start':
        roommsg = input("If you want to see a list of rooms to join type '--show': ")
        if roommsg == '--show':
            response = requests.get(BASE + "rooms")
            print("Rooms:")
            print(response.json())
        else:
            print("You decided not to show rooms.")
        roomchoice = input("Type the room_id of the room you wish to join: ")
        response = requests.get(BASE + "room/" + roomchoice + "/user/" + username)
        if response.status_code == 201:
            print(username + " successfully joined room " + roomchoice)
            while True:
                print("Type '--leave' to leave the room, you'll still be registered to the room.")
                usermessage = input(f"{username}: ")
                if usermessage == '--leave':
                    print("Leaving room " + roomchoice)
                    break
                else:
                    response = requests.put(BASE + "room/" + roomchoice + "/user/" + username + "/message/" + usermessage)
                    if response.status_code != 201 :
                        print("Couldnt send message, something went wrong.")             
        elif response.status_code == 404:
            print("Couldnt join room " + roomchoice + ". No room with that ID.")
        else:
            print("Something went wrong joining room " + roomchoice)
    elif message == '--showmessages':
        roommsg = input("If you want to see a list of rooms to check for messages in type '--show': ")
        if roommsg == '--show':
            response = requests.get(BASE + "rooms")
            print("Rooms:")
            print(response.json())
        else:
            print("You decided not to show rooms.")
        roomchoice = input("Type the room_id of the room you wish to see the messages in: ")
        response = requests.get(BASE + "room/" + roomchoice + "/messages", {"username": username})
        print("Messages in room " + roomchoice + " from " + username + ":")
        print(response.json())
    elif message == '--showmymessages':
        roommsg = input("If you want to see a list of rooms to check for messages in type '--show': ")
        if roommsg == '--show':
            response = requests.get(BASE + "rooms")
            print("Rooms:")
            print(response.json())
        else:
            print("You decided not to show rooms.")
        roomchoice = input("Type the room_id of the room you wish to see the messages in: ")
        response = requests.get(BASE + "room/" + roomchoice + "/user/" + username + "/messages")
        print("Messages in room " + roomchoice + ":")
        print(response.json())