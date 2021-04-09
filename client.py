import random
import sys

import requests

BASE = "http://127.0.0.1:5000/api/"

chatbots = ["bot1", "bot2", "bot3", "bot4"]
picked_chatbot = random.choice(chatbots)

# just so we can make a lot of users
n = random.randint(0, 5000)

#post_user = BASE + "user/", {"username": str(n)}
#print(post_user)
print("User picked " + str(n))
response = requests.post(BASE + "user/" + str(n))
print(response.json())
#Legge til feilhåndtering dersom userid allerede finnes

print("RESULT FROM GET ALL USERS")
response = requests.get(BASE + "users")
print(response.json())

sys.exit()
# ALT SOM STÅR UNDER MÅ BARE INGONERES ;)

print("Welcome ", n, " your user has been created. Please join a room to chat by typing ...")

print()
response = requests.get(BASE + "room/0")
print(response.json())

print("Do you want to join one of the following rooms? [y/n]")

will_join = input()

if will_join == "y":
    print("good")
else:
    print("No is selected. Do you wish to create a room [y/n]")
    create_room = input()
    if create_room == "y":
        print("Good a room will be created for you")
        response = requests.post(BASE + "room/1", {"roomname": "PortfolioWork"})
        print(response.json())
    else:
        print("That is to bad too hear. If you don't want to join or create a room. The program will be closed.")
        print("Feel free to try again")
        sys.exit()

""""
Bruker er laget
Sjekke om det finnes rom
Deretter må den joines et rom
Når i et rom. mulighet til å sende melding
Og thread som sjekkerom det har kommet nye meldinger

"""

""""
først en bruker
Deretter må den joines et rom
Når i et rom. mulighet til å sende melding
Og thread som sjekkerom det har kommet nye meldinger

"""
"""""
print("-------------------------------------------------------")
print("RESULT FROM POST A USER")
response = requests.post(BASE + "user/0", {"username": "oyvind91", "usertype": "admin"})
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM POST A USER")
response = requests.post(BASE + "user/1", {"username": "someone", "usertype": "regular"})
print(response.json())
"""""

print("-------------------------------------------------------")
print("RESULT FROM GET A USER")
response = requests.get(BASE + "user/0")
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM GET A USER")
response = requests.get(BASE + "user/1")
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM GET ALL USERS")
response = requests.get(BASE + "users")
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM POST A ROOM")
response = requests.post(BASE + "room/0", {"roomname": "ObligWork"})
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM POST THE SAME ROOM_ID")
response = requests.post(BASE + "room/0", {"roomname": "ObligWork"})
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM POST A ROOM")
response = requests.post(BASE + "room/1", {"roomname": "PortfolioWork"})
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM GET A ROOM")
response = requests.get(BASE + "room/0")
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM GET ALL ROOMS")
response = requests.get(BASE + "rooms")
print(response.json())
