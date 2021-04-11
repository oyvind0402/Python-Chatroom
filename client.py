from threading import Timer

import requests
import time
import sys
import random


print("----------------------------------------------")
print("Welcome to the electric boogaloo API chatroom!")
print("----------------------------------------------")

#TODO Bots

BASE = "http://127.0.0.1:5000/api/"


while True:
    try:
        username = input("Type in your username: ")
        response = requests.post(BASE + "user/" + username)
        if response.status_code == 201:
            print("User created with username: " + username)
            break
        elif response.status_code == 409:
            print("A user already exists with that username, try another name.")
            continue
    except (EOFError, KeyboardInterrupt):
        print(" You have chosen to end the chat and that is your loss")
        sys.exit()
    except TimeoutError:
        print(" You're slow. Bye.")
        sys.exit()
    except EOFError:
        print(" Oh no! Something's wrong. Bye :'(")
        sys.exit()


print("Thanks for joining the server! Type --help for a list of commands.")

def def_pass():
    pass

def chatroom(room_id):
    room_id = str(room_id)
    in_room = True
    message_input = ""
    print(f"You are now in the room {room_id}")
    print("For help, type '--help'.")

    while in_room:
        # timeout = 5.0
        # timer_thread = Timer(timeout, def_pass)
        # timer_thread.start()
        # try:
        message_input = input(username + " to room " + room_id + ": ")
        # timer_thread.cancel()
        # print("timer cancelled")

        if message_input == "--exit":
            print(f"----- You have exited room {room_id} ------")
            print("You are back in the main terminal.")
            break
        elif message_input== "--help":
             print("Type '--help' to show this help prompt\nType '--showmessages' to show all messages in this chatroom\nType '--exit' to leave the chatroom and go back to the main terminal.")
        elif message_input == "--showmessages":
            response = requests.get(BASE + "room/" + str(room_id) + "/user/" + username + "/messages", {"username": username})
            print(response.json())
        else:
            response = requests.put(BASE + "room/" + str(room_id) + "/user/" + username + "/message/" + message_input, {"username": username})

def choose_room_prompt(username):
    roomchoice = input("Type the room ID. (To see a list of all rooms, type '--show'): ")
    if roomchoice == '--show':
        response = requests.get(BASE + "rooms", {"username": username})
        print("Rooms:")
        print(response.json())
        roomchoice = input("Type the room_id of the room you wish to join: ")
    return roomchoice

#TODO Get one room only
#TODO Get all room user for one room
#TODO Be able to request other users

while True:
    try:
        message = input(f'{username}: ')
        if message == '--help':
            print("Type '--create' to create a chat room\nType '--help' to show this help prompt\nType '--showrooms' " + 
            "to show all rooms\nType '--start' to join a chatroom to start typing messages\nType '--join' to join a chatroom\n" +
            "Type '--showmessages' to show all messages for a specific chatroom\nType '--showmymessages' to show all your messages for a specific chatroom.\nType '--exit' to leave the program. This will delete your user.")
        elif message == '--create':
            while True:
                roomname = input("Type in the roomname: ")
                roomid = (hash(roomname) % 256)
                response = requests.post(BASE + "room/" + str(roomid), {"roomname": roomname, "username": username})
                if response.status_code == 201:
                    print("Chat room called " + roomname + " created.")
                    joinmessage = input("Do you wish to join the room you just created?: ")
                    joinmessage = joinmessage.lower()
                    if joinmessage == 'y' or joinmessage == 'yes':
                        response = requests.put(BASE + "room/" + str(roomid) + "/user/" + username, {"username": username})
                        print("Joined " + roomname)
                        chatroom(roomid)
                        break
                    elif joinmessage == 'n' or joinmessage == 'no':
                        break
                elif response.status_code == 409:
                    print("A room already exists with that roomname, try again.")
                    continue
                elif response.status_code == 404:
                    print("Wrong syntax for the roomname")
        elif message == '--showrooms':
            response = requests.get(BASE + "rooms", {"username": username})
            print("Rooms:")
            print(response.json())
        elif message == '--join':
            roomchoice = choose_room_prompt(username)
            response = requests.put(BASE + "room/" + roomchoice + "/user/" + username, {"username": username})
            if response.status_code == 201:
                print(username + " successfully joined room " + roomchoice)
                chatroom(roomchoice)
            elif response.status_code == 404:
                print("Couldnt join room " + roomchoice + ". No room with that ID.")
            else:
                print("Something went wrong joining room " + roomchoice)
        elif message == '--start':
            roomchoice = choose_room_prompt(username)
            response = requests.get(BASE + "room/" + roomchoice + "/user/" + username, {"username": username})
            if response.status_code == 201:
                print(username + " successfully joined room " + roomchoice)
                while True:
                    print("Type '--leave' to leave the room, you'll still be registered to the room.")
                    usermessage = input(f"{username}: ")
                    if usermessage == '--leave':
                        print("Leaving room " + roomchoice)
                        break
                    else:
                        response = requests.put(BASE + "room/" + roomchoice + "/user/" + username + "/message/" + usermessage, {"username": username})
                        if response.status_code != 201 :
                            print("Couldnt send message, something went wrong.")             
            elif response.status_code == 404:
                print("Couldnt join room " + roomchoice + ". No room with that ID.")
            else:
                print("Something went wrong joining room " + roomchoice)
        elif message == '--showmymessages':
            print("You need to choose a room in order to see your messages.")
            roomchoice = choose_room_prompt(username)
            response = requests.get(BASE + "room/" + roomchoice + "/messages", {"username": username})
            print("Messages in room " + roomchoice + " from " + username + ":")
            print(response.json())
        elif message == '--showmessages':
            print("You need to choose a room to check for messages.")
            rroomchoice = choose_room_prompt(username)
            response = requests.get(BASE + "room/" + roomchoice + "/user/" + username + "/messages", {"username": username})
            print("Messages in room " + roomchoice + ":")
            print(response.json())
        elif message == '--exit':
            print("Are you sure you want to exit? This will DELETE your user!")
            answer = input("Y(es) or N(o): ")
            answer = answer.lower()
            if answer == "y" or answer == "yes":
                response = requests.delete(BASE + "user/" + username, data={"username": username})
                sys.exit("You have exited the program. Goodbye.")
            elif answer == "n" or answer == "no":
                continue
            else:
                print("Invalid input. You will be taken back to the main terminal.")
    except (EOFError, KeyboardInterrupt):
        print("\nYou have chosen to leave the program and that is your loss. \nYour user is being deleted as revenge.")
        response = requests.delete(BASE + "user/" + username, data={"username": username})
        sys.exit()
    except TimeoutError:
        print("\nYou're slow. Bye. \nPS: Your user has been deeeeeleeeeeeteeeeeed.")
        response = requests.delete(BASE + "user/" + username, data={"username": username})
        sys.exit()
    except EOFError:
        print("\nOh no! Something's wrong. Bye :'( \nPS: Your user has been erased from our hearts.")
        response = requests.delete(BASE + "user/" + username, data={"username": username})
        sys.exit()