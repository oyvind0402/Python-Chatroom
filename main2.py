import json

from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

user_post_args = reqparse.RequestParser()
user_post_args.add_argument("username", type=str, help="Username is required...", required=True)
# user_post_args.add_argument("usertype", type=str, help="Invalid syntax for usertype...", required=False)

room_post_args = reqparse.RequestParser()
room_post_args.add_argument("room_id", type=int, help="Room id is required...", required=True)

room_user_put_args = reqparse.RequestParser()
room_user_put_args.add_argument("room_id", type=int, help="Room id is required...", required=True)
room_user_put_args.add_argument("user_name", type=str, action="append", required=True)

room_user_get_args = reqparse.RequestParser()
room_user_get_args.add_argument("room_id", type=int, help="Room id is required...", required=True)

message_put_args = reqparse.RequestParser()
message_put_args.add_argument("room_id", type=int, help="Room id is required...", required=True)
message_put_args.add_argument("user_name", type=str, help="Username is required", required=True)
message_put_args.add_argument("message", type=str, action="append", help="Message cannot be empty", required=True)

message_get_args = reqparse.RequestParser()
message_get_args.add_argument("room_id", type=int, help="Room id is required...", required=True)
message_get_args.add_argument("username", type=str, help="Room id is required...", required=True)

users = []
rooms = {}

'''
[
    {'roomid': 0,
    'userlist': ['user0', 'user1'],
    'message_list': [msg, msg]
        ]
    }
]

{
    0 : {
        'userlist' : [user0, user1]
        'message_list':[msg, msg]
    }
}
'''

# Create post args for messages

def abort_if_user_not_exists(username):
    if username not in users:
        abort(404, message=f"Could not find user \"{username}\"")

def abort_if_user_exists(username):
    if username in users:
        abort(409, message=f"User already exists with ID \"{username}\"")

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

def abort_if_message_list_empty(room_id):
    if len(rooms[room_id]["message_list"]) == 0:
        abort(404, message=f"Could not find any messages for room {room_id}")

class User(Resource):
    def get(self, username=None):
        if username == None:
            return users, 200
        else:
            abort_if_user_not_exists(username)
            if username in users:
                return username, 200

    def post(self, username):
        abort_if_user_exists(username)
        users.append(username)
        return username, 201

    def delete(self, username):
        abort_if_user_not_exists(username)
        users.remove(username)
        return '', 204


class Room(Resource):
    def get(self, room_id=None):
        if room_id is None:
            return rooms, 200
        else:
            room_id = str(room_id)
            abort_if_room_not_exists(room_id)
            return rooms[room_id], 200

    def put(self, room_id):
        room_id = str(room_id)
        abort_if_room_exists(room_id)
        room = {"userlist": [], "message_list": []}
        rooms[room_id]= room
        return room_id, 201


class RoomUser(Resource):

    def get(self, room_id, username=None):
        room_id = str(room_id)

        abort_if_room_not_exists(room_id)
        if username is None:
            return rooms[room_id]["userlist"], 201
        else:
            abort_if_room_empty(room_id)
            abort_if_user_not_exists(username)
            abort_if_roomuser_not_exists(room_id, username)
            return username + " is in the room " + str(room_id), 201


    def put(self, room_id, username):
        room_id = str(room_id)

        abort_if_user_not_exists(username)
        abort_if_room_not_exists(room_id)
        abort_if_roomuser_exists(room_id, username)
        rooms[room_id]["userlist"].append(username)
        return username + " is connected to " + str(room_id), 201


class Message(Resource):
    def get(self, room_id, username):
        room_id = str(room_id)

        abort_if_room_not_exists(room_id)
        abort_if_roomuser_not_exists(room_id, username)
        abort_if_message_list_empty(room_id)
        return rooms[room_id]["message_list"], 201                

    def post(self, room_id, username):
        return

    def put(self, room_id, username, message):
        room_id = str(room_id)

        abort_if_room_not_exists(room_id)
        abort_if_roomuser_not_exists(room_id, username)
        rooms[room_id]["message_list"].append(message)
        return message, 201


api.add_resource(User, "/api/user/<string:username>", "/api/users")
api.add_resource(Room, "/api/room/<int:room_id>", "/api/rooms")
api.add_resource(RoomUser, "/api/room/<int:room_id>/user/<string:username>", "/api/room/<int:room_id>/users")
api.add_resource(Message, "/api/room/<int:room_id>/user/<string:username>/message/<string:message>", "/api/room/<int:room_id>/user/<string:username>/messages")


@app.route('/')
def index():
    return "SHITTY OBLIG 2"


if __name__ == "__main__":
    app.run(debug=True)
