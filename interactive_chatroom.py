import socket
import threading
from threading import Timer
from client import *

#Unused imports at the moment, they were a part of our attempt at push notifications.
#from keyboard import press_and_release
#from apscheduler.schedulers.background import BackgroundScheduler

import requests
import time
import sys
import socket
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
        response = add_user(username)
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

def listening(room_id):
    # We used this to test to run several threads
    # However it seems that we cannot run this function and the chatroom at the same time.
    # We think this is because threads depends on I/O and since def listening is constant running this messes thing up
    # We also used a timed thread but but this doesn't change the fact that input() is blocking and therefor not working
    # The only solution (we could think of) would be a push from the server
    # but unfortunately we didnt get this to work either (see server.py)
    IP = "127.0.0.2"
    port = 5001

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP, port))
    client.send(username.encode())

    # True would be replaced with a global variable like in_chat_room = True to make the thread stop at the same time
    # as the chatroom but since it wasn't working at all there was no point in implementing this
    while True:
        # Both solution weren't working ...

        # new_message = client.recv(1024).decode()
        # print(new_message)

        response = requests.get(BASE + "room/" + str(room_id) + "/user/" + username + "/messages", {"username": username})
        print(response.json())
        time.sleep(10)


#Function to use the keyboard.press_and_release import, which presses enter. Unused atm, it was part of an unsuccessful attempt at push notifications.
# def enter():
#     press_and_release('enter')


def chatroom(room_id):
    room_id = str(room_id)
    # Part of the code we didnt make work - keeping it here to show we tried implementing push notifications.
    # listening_thread = threading.Thread(target=listening(room_id))
    # listening_thread.start()

    # timed thread:
    # timeout = 5
    # listen_timed = threading.Timer(timeout, listening(room_id))
    # listen_timed.start()
    # listen_timed.cancel()

    # Another solution we came up with was signal which would have been perfect to set a timer on a while loop
    # This however only works on linux ...

    print(f"You are now in room {room_id}")
    print("For help, type '--help'.\nTo see new messages press enter/return without typing anything.")
    readmessages = []

    while True:
        try:
            response = requests.get(BASE + "room/" + str(room_id) + "/user/" + username + "/messages", {"username": username})
            initialmessage = response.json()

            #Adding a background scheduler to press enter every 10 seconds to update the chat to see new messages.
            #Basically polling every 10 seconds for new messages because the input is a blocking call stopping us
            #from updating the get request for all messages in the chatroom.
            #This was our way of doing push notifications - instead of pressing enter it could also be sending a message like "A new message has appeared in your chat room, press enter to see it."
            #The problem with this is that if you're running two terminals on the same computer it can only emulate one enter keypress and it will continue doing it untill you do a press of enter in
            #The initial terminal the background process started in. So it will continue pressing enter every 10 seconds in any active window, even outside of the program.
            #We decided not to use it because of this fault in the process in combination with our program. Having it continually press enter untill it does it in the right window isnt a good way to deal with it.

            #scheduling = False
            if response.status_code == 200:
                #Unused code for the background scheduler pressing enter (through the enter function)
                # if len(initialmessage) > len(readmessages):
                #     scheduler = BackgroundScheduler()
                #     scheduler.start()
                #     scheduling = True
                #     scheduler.add_job(enter, 'interval', seconds=10)


                for i in range(len(readmessages), len(response.json())):
                    user = response.json()[i]["username"]
                    msg = response.json()[i]["message"]
                    if user != username:
                        print(user + f" to room {room_id}: " + msg)
                readmessages = response.json()
            message_input = input(username + " to room " + room_id + ": ")
            message_input = message_input.strip()
            # if scheduling == True:
            #     scheduler.shutdown()
            #     scheduling = False
            # timer_thread.cancel()
            if message_input == "--exit":
                print(f"----- You have exited room {room_id} ------")
                print("You are back in the main terminal")
                # user gets deleted when leaving the room
                break
            elif message_input== "--help":
                 print("Type '--help' to show this help prompt\n" +
                 "Press enter/return without typing anything to update the chatroom to see new messages.\n"+
                 "Type '--showmessages' to show all messages in this chatroom\n"+
                 "Type '--showmymessages' to see your messages in this chatroom\n"+
                 "Type '--exit' to leave the chatroom and go back to the main terminal\n"+
                 "Type '--removeme' to remove yourself from this chatroom")
            elif message_input == "--showmessages":
                response = get_all_messages(room_id, username, username)
                print(response.json())
            elif message_input == "--showmymessages":
                response = get_messages(room_id, username)
                print("Messages in room " + str(room_id) + " from " + username + ":")
                print(response.json())
            elif message_input == "--removeme":
                answer = input("Are you sure you want to REMOVE yourself from this room? y/[N] ")
                answer = answer.lower()
                if answer == 'y' or joinmessage == 'yes':
                    delete_roomuser(room_id, username, username)
                    break       
                else:
                    print("If it's not a yes, then you stay")
                    continue
            else:
                if len(message_input) < 1:
                    continue
                else:
                    add_message(room_id, username, message_input, username)
        except (EOFError, KeyboardInterrupt):
            print("\nYou have chosen to leave the room, but you are still in its userlist. \nPress ctrl c again to leave the entire program and delete your user.")
            break
        except:
            print("\nThere was an unknown error. You are being deleted and logged out.")
            response = delete_user(username, username)
            sys.exit()

def choose_room_prompt(username):
    roomchoice = input("Type the room ID. (To see a list of all rooms, type '--show'): ")
    if roomchoice.strip() == '--show':
        response = get_all_rooms(username)
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
                response = add_room(roomid, roomname, username)
                if response.status_code == 201:
                    print("Chat room called " + roomname + " created.")
                    joinmessage = input("Do you wish to join the room you just created? y/[N]: ")
                    joinmessage = joinmessage.lower()
                    if joinmessage == 'y' or joinmessage == 'yes':
                        response = add_roomuser(roomid, username, username)
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
            searched_user = check_if_followed_by_argument(username, '--userinfo', message, None, True)
            response = get_user(searched_user, username)
            print(response.json())
        elif message == '--showusers':
            response = get_all_users(username)
            print("The following users are currently online:")
            print(response.json())
        elif message == '--showrooms':
            response = get_all_rooms(username)
            print("Rooms:")
            print(response.json())
        elif message.startswith('--showroomusers'):
            roomchoice = check_if_followed_by_argument(username, '--showroomusers', message)
            response = get_all_roomusers(roomchoice, username)
            print(response.json())
        elif message.startswith('--showroom'):
            roomchoice = check_if_followed_by_argument(username, '--showroom', message)
            response = get_room(roomchoice, username)
            print(response.json())
        elif message.startswith('--join'):
            roomchoice = check_if_followed_by_argument(username, '--join', message)
            response = add_roomuser(roomchoice, username, username)
            response2 = get_roomuser(roomchoice, username, username)
            if response.status_code == 201 or response2.status_code == 201:
                print(username + " successfully joined room " + roomchoice)
                chatroom(roomchoice)
            elif response.status_code == 404:
                print("Couldn't join room " + roomchoice)
            else:
                print(response.json())
        elif message.startswith('--showmymessages'):
            roomchoice = check_if_followed_by_argument(username, '--showmymessages', message, "You need to choose a room in order to see your messages.")
            response = get_messages(roomchoice, username)
            if response.status_code == 200:
                print("Messages in room " + roomchoice + " from " + username + ":")
                print(response.json())
            else:
                print("Couldn't show messages from room " + roomchoice)
        elif message.startswith('--showmessages'):
            roomchoice = check_if_followed_by_argument(username, '--showmessages', message, "You need to choose a room to check for messages.")
            response = get_all_messages(roomchoice, username, username)
            if response.status_code == 200:
                print("Messages in room " + roomchoice + ":")
                print(response.json())
            else:
                print("Couldn't show messages from room " + roomchoice + ". No room with that ID.")
        elif message == '--exit':
            print("Are you sure you want to exit? This will DELETE your user!")
            answer = input("y/[N]: ")
            answer = answer.lower()
            if answer == "y" or answer == "yes":
                response = delete_user(username, username)
                sys.exit("You have exited the program. Goodbye.")
            elif answer == "n" or answer == "no":
                continue
            else:
                print("Invalid input. You will be taken back to the main terminal.")
        else:
            print("Not a command, dummy. If you need help, type '--help'")
    except (EOFError, KeyboardInterrupt):
        print("\nYou have chosen to leave the program and that is your loss. \nYour user is being deleted as revenge.")
        response = delete_user(username, username)
        sys.exit()
    except TimeoutError:
        print("\nYou're slow. Bye. \nPS: Your user has been deeeeeleeeeeeteeeeeed.")
        response = delete_user(username, username)
        sys.exit()
    except:
        print("\nOh no! Something's wrong. Bye :'( \nPS: Your user has been erased from our hearts.")
        response = delete_user(username, username)
        sys.exit()

        