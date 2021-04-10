import requests

BASE = "http://127.0.0.1:5000/api/"

print("-------------------------------------------------------")
print("RESULT FROM POST A USER")
response = requests.post(BASE + "user/oyvind91")
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM POST A USER")
response = requests.post(BASE + "user/someone")
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM GET A USER")
response = requests.get(BASE + "user/oyvind91")
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM GET A USER")
response = requests.get(BASE + "user/someone")
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM GET ALL USERS")
response = requests.get(BASE + "users")
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM POST A ROOM")
response = requests.post(BASE + "room/0")
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM POST a ROOM_ID")
response = requests.post(BASE + "room/1")
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM POST A ROOM")
response = requests.post(BASE + "room/2")
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM GET A ROOM")
response = requests.get(BASE + "room/0")
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM GET ALL ROOMS")
response = requests.get(BASE + "rooms")
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM put A ROOMUSER")
response = requests.put(BASE + "room/0" + "/user/" + "oyvind91")
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM put A ROOMUSER")
response = requests.put(BASE + "room/0" + "/user/" + "oyvind91")
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM put A ROOMUSER")
response = requests.put(BASE + "room/0" + "/user/" + "someone")
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM GET A ROOM")
response = requests.get(BASE + "room/0")
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM GET A ROOM")
response = requests.get(BASE + "room/1")
print(response.json())

# print("-------------------------------------------------------")
# print("RESULT FROM POST A ROOMUSER")
# response = requests.post(BASE + "room/0" + "/oyvind91")
# print(response.json())

# print("-------------------------------------------------------")
# print("RESULT FROM POST A ROOMUSER")
# response = requests.post(BASE + "room/0", {"username": "someone"})
# print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM GET ROOMUSERS")
response = requests.get(BASE + "room/0/user/someone")
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM GET ALL ROOMUSERS")
response = requests.get(BASE + "room/0/users")
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM GET ROOMUSERS")
response = requests.get(BASE + "room/1/users")
print(response.json())

# print("-------------------------------------------------------")
# print("RESULT FROM POST A ROOMUSER")
# response = requests.post(BASE + "room/1/users", {"user_id": 0})
# print(response.json())

# print("-------------------------------------------------------")
# print("RESULT FROM POST A ROOMUSER")
# response = requests.post(BASE + "room/1/users", {"user_id": 1})
# print(response.json())

#/api/room/<int:room_id>/user/<string:username>/message/<string:message>"
print("-------------------------------------------------------")
print("RESULT FROM PUT MESSAGE TO ROOM 0")
response = requests.put(BASE + "room/0/user/someone/message/hey")
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM PUT MESSAGE TO ROOM 1")
response = requests.put(BASE + "room/1/user/oyvind91/message/hey")
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM GET MESSAGES FROM OYVIND91 IN ROOM 0")
response = requests.get(BASE + "room/0/user/oyvind91/messages")
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM GET MESSAGES FROM NOT_MEMBER IN ROOM 0")
response = requests.get(BASE + "room/0/user/not_member/messages")
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM GET MESSAGES FROM NOT_MEMBER IN ROOM 1")
response = requests.get(BASE + "room/1/user/not_member/messages")
print(response.json())

#"/api/room/<int:room_id>/messages"

#Add more tests with possibility to fail