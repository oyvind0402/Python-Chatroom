import requests

BASE = "http://127.0.0.1:5000/api/"

print("-------------------------------------------------------")
print("RESULT FROM POST")
response = requests.post(BASE + "user/0", {"username": "oyvind91", "usertype": "admin"})
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM POST")
response = requests.post(BASE + "user/1", {"username": "someone", "usertype": "regular"})
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM GET")
response = requests.get(BASE + "user/0")
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM GET")
response = requests.get(BASE + "user/1")
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM POST")
response = requests.post(BASE + "room/0", {"roomname": "ObligWork"})
print(response.json())

print("-------------------------------------------------------")
print("RESULT FROM GET")
response = requests.get(BASE + "room/0")
print(response.json())
