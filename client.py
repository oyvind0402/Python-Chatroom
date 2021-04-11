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
        username = username.strip()
        response = requests.post(BASE + "user/" + username)
        if response.status_code == 201:
            print("User created with username: " + username)
            break
        elif response.status_code == 409:
            print("A user already exists with that username, try another name.")
            continue
    except (EOFError, KeyboardInterrupt):
        print("\nYou have chosen to end the chat and that is your loss")
        sys.exit()
    except TimeoutError:
        print("\nYou're slow. Bye.")
        sys.exit()
    except EOFError:
        print("\nOh no! Something's wrong. Bye :'(")
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
        message_input = message_input.strip()
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
        elif message_input == "--showmymessages":
            response = requests.get(BASE + "room/" + str(room_id) + "/messages", {"username": username}) 
            print("Messages in room " + str(room_id) + " from " + username + ":")
            print(response.json())
        else:
            if len(message_input) < 1:
                continue
            else:
                response = requests.put(BASE + "room/" + str(room_id) + "/user/" + username + "/messages", {"username": username, "message": message_input})

def choose_room_prompt(username):
    roomchoice = input("Type the room ID. (To see a list of all rooms, type '--show'): ")
    if roomchoice.strip() == '--show':
        response = requests.get(BASE + "rooms", {"username": username})
        print("Rooms:")
        print(response.json())
        roomchoice = input("Type the room_id of the room you wish to join: ")
    return roomchoice.strip()

def check_if_followed_by_argument(username, command, message, to_print=None, user_search=False):
    length = len(command)
    argument = message[length:]
    argument = argument.strip()
    if len(message) == length:
        if user_search == False:
            if to_print != None:
                print(to_print)
            argument = choose_room_prompt(username)
        else:
            if to_print != None:
                print(to_print)
            argument = input("Type the username to search: ")  
    return argument

#TODO Be able to request other users


while True:
    try:
        message = input(f'{username}: ')
        message = message.strip()
        if message == '--help':
            print("Type '--create' to create a chat room\n" + 
            "Type '--help' to show this help prompt\n" + 
            "Type '--join [roomid]' to enter a chatroom\n" +
            "Type '--showrooms' to show all rooms\n" + 
            "Type '--showroom [roomid]' to show a specific room's details\n" +
            "Type '--showroomusers [roomid]' to show all users of a specific room\n" +
            "Type '--showmessages [roomid]' to show all messages for a specific chatroom\n" +
            "Type '--showmymessages [roomid]' to show all your messages for a specific chatroom.\n" +
            "Type '--showusers' to show all users online\n" +
            "Type '--userinfo [username]' to see if a user is online\n" +  
            "Type '--exit' to leave the program. This will delete your user.")
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
                    else:
                        print("That did not seem like a yes. You have not been added to the room. If you wish to goin it, use '--join'")
                elif response.status_code == 409:
                    print("A room already exists with that roomname, try again.")
                    continue
                elif response.status_code == 404:
                    print("Wrong syntax for the roomname")
        elif message.startswith('--userinfo'):
            searching_user = check_if_followed_by_argument(username, '--userinfo', message, None, True)
            response = requests.get(BASE + "user/" + searching_user, {"username": username})
            print(response.json())
        elif message == '--showusers':
            response = requests.get(BASE + "users", {"username": username})
            print("The following users are currently online:")
            print(response.json())
        elif message == '--showrooms':
            response = requests.get(BASE + "rooms", {"username": username})
            print("Rooms:")
            print(response.json())
        elif message.startswith('--showroomusers'):
            roomchoice = check_if_followed_by_argument(username, '--showroomusers', message)
            response = requests.get(BASE + "room/" + roomchoice + "/users", {"username": username})
            print(response.json())
        elif message.startswith('--showroom'):
            roomchoice = check_if_followed_by_argument(username, '--showroom', message)
            response = requests.get(BASE + "room/" + roomchoice, {"username": username})
            print(response.json())
        elif message.startswith('--join'):
            roomchoice = check_if_followed_by_argument(username, '--join', message)
            response = requests.put(BASE + "room/" + roomchoice + "/user/" + username, {"username": username})
            response2 = requests.get(BASE + "room/" + roomchoice + "/user/" + username, {"username": username})
            if response.status_code == 201 or response2.status_code == 201:
                print(username + " successfully joined room " + roomchoice)
                chatroom(roomchoice)
            elif response.status_code == 404:
                print("Couldnt join room " + roomchoice + ". No room with that ID.")
            else:
                print(response.json())
        elif message.startswith('--showmymessages'):
            roomchoice = check_if_followed_by_argument(username, '--showmymessages', message, "You need to choose a room in order to see your messages.")
            response = requests.get(BASE + "room/" + roomchoice + "/messages", {"username": username}) 
            print("Messages in room " + roomchoice + " from " + username + ":")
            print(response.json())
        elif message.startswith('--showmessages'):
            roomchoice = check_if_followed_by_argument(username, '--showmessages', message, "You need to choose a room to check for messages.")
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
        else:
            print("Not a command, dummy. If you need help, type '--help'")
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

        