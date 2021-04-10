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

# print("-------------------------------------------------------")
# print("RESULT FROM POST A ROOMUSER")
# response = requests.post(BASE + "room/1/users", {"user_id": 0})
# print(response.json())

# print("-------------------------------------------------------")
# print("RESULT FROM POST A ROOMUSER")
# response = requests.post(BASE + "room/1/users", {"user_id": 1})
# print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM GET ROOMUSERS")
response = requests.get(BASE + "room/1/users")
print(response.json())

