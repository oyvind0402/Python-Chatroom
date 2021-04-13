import json
import socket
import sys
import threading
import time
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

"""REQUEST PARSING SECTION"""
"""Creates request parser for JSON data sent through requests"""
user_get_args = reqparse.RequestParser()
user_get_args.add_argument("username", type=str, help="Username is required", required=True)

user_delete_args = reqparse.RequestParser()
user_delete_args.add_argument("username", type=str, help="Username is required", required=True)

room_post_args = reqparse.RequestParser()
room_post_args.add_argument("roomname", type=str, help="Roomname is required.", required=True)
room_post_args.add_argument("username", type=str, help="Username is required", required=True)

room_get_args = reqparse.RequestParser()
room_get_args.add_argument("username", type=str, help="Username is required", required=True)

room_user_put_args = reqparse.RequestParser()
room_user_put_args.add_argument("username", type=str, help="Username is required", required=True)

room_user_get_args = reqparse.RequestParser()
room_user_get_args.add_argument("username", type=str, help="Username is required", required=True)

room_user_delete_args = reqparse.RequestParser()
room_user_delete_args.add_argument("username", type=str, help="Username is required", required=True)

message_put_args = reqparse.RequestParser()
message_put_args.add_argument("username", type=str, help="Username is required", required=True)
message_put_args.add_argument("message", type=str, help="Message cannot be empty", required=True)

message_get_args = reqparse.RequestParser()
message_get_args.add_argument("username", type=str, help="Username is required", required=False)

users = []  
"""User structure
["item", "item"]
"""

rooms = {}
'''
Rooms structure
{
    0 : {
        'roomname': name,
        'userlist' : [user0, user1]
        'message_list':[msg, msg]
    }
}
'''


"""ABORT SECTION"""
"""Identifies different situations in which program needs to abort and defines response."""
def abort_if_user_not_exists(username):
    if username not in users:
        abort(404, message=f"Could not find user \"{username}\"")


def abort_if_user_exists(username):
    if username in users:
        abort(409, message=f"User already exists with ID \"{username}\"")

def abort_if_querier_does_not_match_user(querier, username):
    if querier != username:
        abort(401, message=f"You can only perform this action for your own user.")


def abort_if_room_not_exists(room_id):
    if room_id not in rooms:
        abort(404, message=f"Could not find room {room_id}")


def abort_if_room_exists(room_id):
    if room_id in rooms:
        abort(409, message=f"Room already exists with ID {room_id}")


def abort_if_room_empty(room_id):
    if len(rooms[room_id]["userlist"]) == 0:
        abort(404, message=f"Could not find any users for room {room_id}.")


def abort_if_roomuser_not_exists(room_id, username):
    if username not in rooms[room_id]["userlist"]:
        abort(404, message=f"User \"{username}\" was not found in room {room_id}")


def abort_if_roomuser_exists(room_id, username):
    if username in rooms[room_id]["userlist"]:
        abort(409, message=f"User \"{username}\" is already in room {room_id}")

def abort_if_roomuser_does_not_exists(room_id, username):
    if username not in rooms[room_id]["userlist"]:
        abort(409, message=f"User \"{username}\" is not in room {room_id}")


def abort_if_message_list_empty(room_id):
    if len(rooms[room_id]["message_list"]) == 0:
        abort(404, message=f"Could not find any messages for room {room_id}")

def abort_if_querier_not_in_room(querier, room_id):
    if room_id not in rooms:
        abort(404, message=f"Could not find room {room_id}")
    if querier not in rooms[room_id]['userlist']:
        abort(401, message=f"You must be part of this room to query it.")


"""RESOURCES SECTION"""
"""Defines resources"""

class User(Resource):
    """Gets one or all users"""
    def get(self, username=None):
        querier = user_get_args.parse_args()
        querier = querier['username']
        abort_if_user_not_exists(querier)

        if username == None:
            return users, 200
        else:
            abort_if_user_not_exists(username)
            if username in users:
                return f"User \"{username}\" is online", 200

    """Adds one user"""
    def post(self, username):
        abort_if_user_exists(username)
        users.append(username)
        return username, 201

    """Deletes one user"""
    def delete(self, username):
        querier = user_delete_args.parse_args()
        querier = querier['username']
        abort_if_querier_does_not_match_user(querier, username)
        abort_if_user_not_exists(username)
        users.remove(username)
        for room_id in rooms:
            if username in rooms[room_id]['userlist']:
                rooms[room_id]['userlist'].remove(username)
        return '', 204


class Room(Resource):
    """Gets one or all rooms"""
    def get(self, room_id=None):
        querier = room_get_args.parse_args()
        querier = querier['username']
        abort_if_user_not_exists(querier)
        if room_id is None:
            formatted_rooms = {}
            for key in rooms:
                formatted_rooms[key] = {"roomname": rooms[key]['roomname'], "userlist": rooms[key]['userlist']}
            return formatted_rooms, 200
        else:
            room_id = str(room_id)
            abort_if_room_not_exists(room_id)
            
            if querier in rooms[room_id]['userlist']:
                """If user who made the room request is in room, display all data"""
                room_resp = rooms[room_id]
            
            else:
                """Else, do not display messages"""
                room_resp = {room_id : {"roomname": rooms[room_id]['roomname'], "userlist": rooms[room_id]['userlist']}}
            return room_resp, 200

    """Creates a new room (must have a unique room ID)"""
    def post(self, room_id):
        querier = room_post_args.parse_args()
        querier = querier['username']
        abort_if_user_not_exists(querier)

        room_id = str(room_id)
        abort_if_room_exists(room_id)
        args = room_post_args.parse_args()

        room = {"roomname": args["roomname"], "userlist": [], "message_list": []}
        rooms[room_id] = room
        return room_id, 201


class RoomUser(Resource):       #RoomUser = user in relation to a room
    """Gets one or all roomusers"""
    def get(self, room_id, username=None):
        querier = room_user_get_args.parse_args()
        querier = querier['username']
        abort_if_user_not_exists(querier)

        room_id = str(room_id)

        abort_if_room_not_exists(room_id)
        if username is None:
            return rooms[room_id]["userlist"], 201
        else:
            abort_if_room_empty(room_id)
            abort_if_user_not_exists(username)
            abort_if_roomuser_not_exists(room_id, username)
            return username + " is in the room " + str(room_id), 201

    """Adds one user to room"""
    def put(self, room_id, username):
        querier = room_user_put_args.parse_args()
        querier = querier['username']
        abort_if_querier_does_not_match_user(querier, username)
        room_id = str(room_id)

        abort_if_user_not_exists(username)
        abort_if_room_not_exists(room_id)
        abort_if_roomuser_exists(room_id, username)
        rooms[room_id]["userlist"].append(username)
        return username + " is connected to " + str(room_id), 201

    """Deletes one user from room"""
    def delete(self, room_id, username):
        querier = room_user_delete_args.parse_args()
        querier = querier['username']
        abort_if_querier_does_not_match_user(querier, username)
        room_id = str(room_id)

        abort_if_user_not_exists(username)
        abort_if_room_not_exists(room_id)
        abort_if_roomuser_does_not_exists(room_id, username)
        rooms[room_id]["userlist"].remove(username)
        return username + " is removed from " + str(room_id), 201


class Message(Resource):
    """Gets messages from one or all users in a room"""
    def get(self, room_id, username=None): 
        room_id = str(room_id) 
        querier = message_get_args.parse_args() 
        abort_if_querier_not_in_room(querier['username'], room_id)
        args = message_get_args.parse_args() 
        if username is not None: 
            abort_if_room_not_exists(room_id) 
            abort_if_roomuser_not_exists(room_id, username) 
            abort_if_message_list_empty(room_id) 
            return rooms[room_id]["message_list"], 200 
        else: 
            username = args["username"] 
            abort_if_room_not_exists(room_id) 
            abort_if_roomuser_not_exists(room_id, username) 
            abort_if_message_list_empty(room_id) 
            usermessages = [] 
            for obj in rooms[room_id]["message_list"]:
                if obj["username"] == username: 
                    usermessages.append(obj["message"]) 
                    return usermessages, 200

    """Adds message to room"""
    def put(self, room_id, username):
        args = message_put_args.parse_args()
        querier = args['username']
        abort_if_querier_does_not_match_user(querier, username)
    
        room_id = str(room_id)

        abort_if_room_not_exists(room_id)
        abort_if_roomuser_not_exists(room_id, username)
        rooms[room_id]["message_list"].append(args)
        return args, 201

"""ROUTE SECTION"""
api.add_resource(User, "/api/user/<string:username>", "/api/users")
api.add_resource(Room, "/api/room/<int:room_id>", "/api/rooms")
api.add_resource(RoomUser, "/api/room/<int:room_id>/user/<string:username>", "/api/room/<int:room_id>/users")
api.add_resource(Message, "/api/room/<int:room_id>/user/<string:username>/messages",
                  "/api/room/<int:room_id>/messages")


@app.route('/')
def index():
    return "OBLIG 2"

"""Part of attempt of implementing push notifications"""
# api_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if __name__ == "__main__":
    """Part of attempt of implementing push notifications"""
    # ip = "127.0.0.2"
    # port = 5001
    # api_server.connect((ip, port))
    # message = "api"
    # api_server.send(message.encode())
    app.run(debug=True)