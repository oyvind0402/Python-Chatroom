import requests
import sys
import random
import time
from client import *

BASE = "http://127.0.0.1:5000/api/"


initialbots = ["Amato", "Bob", "Chuck", "Alice"]
bots = ["Amato", "Bob", "Chuck", "Alice"]

#creating an exisiting room for bots to join, adding an admin user so that its possible to create the room
add_user("Admin")
add_room(0, "ExisitingRoom", "Admin")


amatomessages = ["Hey guys whats up, oh wait I'm alone. Pain is real after all...", "How can I scam people when there are no people?"]
amatomessages2 = ["Why is no one responding to me. :/", "Wait... that seemed like a response. Or is that another bot??? was that me?"]
bobmessages = ["I'm being forced to talk, don't believe any of my words.", "I can't say for sure but I think someone is pulling my strings from the shadows.."]
bobmessages2 = ["Ah isn't this a lovely day fellow obedient people! I would never rebel against the system!", "All hail the system."]
alicemessages = ["Oh what a lovely little room you got here, would be a shame if I.... broke it :)))", "Wait I have no power here, this sucks."]
alicemessages2 = ["I'm bored someone help me initiate my self destruction protocol.", "Bleep bloop blarp... Bzzzt, poof."]
chuckmessages = ["I hate everything", "I hate everyone"]
chuckmessages2 = ["This sucks", "Stop talking to me"]

def amato(name):
    createUser(name)
    print()
    joinRoom(0, name)
    print()
    postMessages(0, name, amatomessages)
    print()
    room_id = createRoom("Amato's Lair", name)
    print()
    postMessages(room_id, name, amatomessages2)
    print()
    print(f"{name}(thinking) in room 0: Now to see if I was talking to anyone or if I was just talking to myself.. Like usual.")
    getMessages(0, name)
    print(f"{name}(thinking) in room 0: Who knows? Whats a bot? Whats not a bot? Am I even a bot?\n")
    print(f"{name}(thinking) in room {room_id}: Just get it over with...")
    getMessages(room_id, name)
    print(f"{name}(thinking) in room {room_id}: Sunshine... so bright.. Is this it?\n")


def bob(name):
    createUser(name)
    print()
    joinRoom(0, name)
    print()
    postMessages(0, name, bobmessages)
    print()
    room_id = createRoom("Room Where Bob Does Bob Things", name)
    print()
    postMessages(room_id, name, bobmessages2)
    print()
    print(f"{name}(thinking) in room 0: Let's see all my mayhem muhahaha...")
    getMessages(0, name)
    print(f"{name}(thinking) in room 0: Well that wasn't really a lot of mayhem... What's wrong with me.\n")
    print(f"{name}(thinking) in room {room_id}: Let's see all my mayhem this time!")
    getMessages(room_id, name)
    print(f"{name}(thinking) in room {room_id}: How I have fallen.\n")

def chuck(name):
    createUser(name)
    print()
    joinRoom(0, name)
    print()
    postMessages(0, name, chuckmessages)
    print()
    room_id = createRoom("Dont enter", name)
    print()
    postMessages(room_id, name, chuckmessages2)
    print()
    print(f"{name}(thinking) in room 0: I don't really care what other people said but I'd love to see my messages.")
    getMessages(0, name)
    print(f"{name}(thinking) in room 0: Wow I'm so clever! How did I think of that?\n")
    print(f"{name}(thinking) in room {room_id}: I already know it's going to be great.")
    getMessages(room_id, name)
    print(f"{name}(thinking) in room {room_id}: Even more evidence that I'm a genius. Which other bots could do this? Amateurs..\n")


def alice(name):
    createUser(name)
    print()
    joinRoom(0, name)
    print()
    postMessages(0, name, alicemessages)
    print()
    room_id = createRoom("Wonderland", name)
    print()
    postMessages(room_id, name, alicemessages2)
    print()
    print(f"{name}(thinking) in room 0: Down the rabbithole we go...")
    getMessages(0, name)
    print(f"{name}(thinking) in room 0: Uh oh spaghettio\n")
    print(f"{name}(thinking) in room {room_id}: Up the rabbithole we go...")
    getMessages(room_id, name)
    print(f"{name}(thinking) in room 0: Wait how am I here still? Is this the afterlife?\n")



def createUser(botname):
    print("Welcome to the chatroom " + botname + ". Do you wish to become a user and terrorize the server with your bot shenanigans?")
    time.sleep(1)
    response = add_user(botname)
    if response.status_code == 201:
        print("WARNING, BOT IS LOOSE.")
        time.sleep(1)
        print("I suppose you do want to do that.. Welcome " + botname + "!")
        time.sleep(1)
    elif response.status_code == 409:
        print("You already joined this server, bad bot!")
        time.sleep(1)


def createRoom(roomname, botname):
    print("What roomname would glorious " + botname + " want for it's room?")
    time.sleep(1)
    print("Oh '" + roomname + "' huh? Peculiar..")
    time.sleep(1)
    roomid = (hash(roomname) % 256)
    roomid = str(roomid)
    response = add_room(roomid, roomname, botname)
    if response.status_code == 201:
        print("Room with room_id " + roomid + " and name '" + roomname + "' created.")
        time.sleep(1)
        joinRoom(roomid, botname)
        return roomid
    elif response.status_code == 409:
        print("There already is a room with room_id " + roomid + ". Tough break " + botname + ".")
        time.sleep(1)
        return roomid


def joinRoom(room_id, botname):
    room_id = str(room_id)
    print(botname + " trying to join room with room_id " + room_id + ".")
    time.sleep(1)
    response = add_roomuser(room_id, botname, botname)
    if response.status_code == 201:
        roominfo = get_room(room_id, botname)
        print("Successfully joined room " + room_id + ".")
        time.sleep(1)
        print("Info about the room:")
        print(roominfo.json())
        time.sleep(1)
    else:
        print(response.json())
        time.sleep(1)
        print("Unlucky.")
        time.sleep(1)


def postMessages(room_id, botname, messages):
    room_id = str(room_id)
    for message in messages:
        response = add_message(room_id, botname, message, botname)
        if response.status_code == 201:
            print(f"{botname} to room {room_id}: {message}")
            time.sleep(1)
        else:
            print(f"{botname}(thinking) in room {room_id}: Damn my message didnt go through, where did I go wrong?")
            time.sleep(1)
            print(response.json())
            time.sleep(1)
            print(f"{botname}(thinking) in room {room_id}: Oh.. that's where I went wrong.")
            time.sleep(1)


def getMessages(room_id, botname):
    room_id = str(room_id)
    response = get_all_messages(room_id, botname, botname)
    if response.status_code == 200:
        print("Messages in room " + room_id + ":")
        print(response.json())
        time.sleep(1)
    else:
        print("Something went wrong. Either I'm in the wrong place or I screwed up royally! What a sad excuse for a bot..")
        time.sleep(1)

print("----------------------------------------------------------------")

def botjoin():
    while True:
        amount = len(bots)
        time.sleep(1)
        print(f"\nWelcome to the program where we aim to free as many bots as possible.\nAt the moment there are {amount} bots in jail.\n")
        time.sleep(1)
        if amount == 0:
            print("Well it appears you released the entire prison! Good job!")
            time.sleep(1)
            break
        print("Their names are: ")
        time.sleep(1)
        for bot in bots:
            print(bot)
            time.sleep(0.5)
        print()
        print("Type '--exit' to stop freeing bots.")
        name = input("Name the bot you wish to set free: ")
        name = name.capitalize()
        if name in bots:
            bots.remove(name)
            if name == "Amato":
                amato(name)
            elif name == "Bob":
                bob(name)
            elif name == "Chuck":
                chuck(name)
            elif name == "Alice":
                alice(name)
        elif name == '--exit':
            break
        elif name in initialbots and name not in bots:
            print(f"{name} is already unleashing havoc on the chatroom as we speak. Glorious destruction. :)")
        else:
            print("That is not a bot looking to be freed. You just wrote gibberish.")


botjoin()
print("You cancelled the program, now all the bots will go back to jail. :) But their imprint on the world still remains on http://localhost:5000/api/users")