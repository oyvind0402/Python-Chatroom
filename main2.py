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
message_put_args.add_argument("message", type=str, action="append", required=True)

message_get_args = reqparse.RequestParser()
message_get_args.add_argument("room_id", type=int, help="Room id is required...", required=True)
message_get_args.add_argument("username", type=str, help="Room id is required...", required=True)

users = []
rooms = []

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
        abort(404, message="Could not find user...")


def abort_if_user_exists(username):
    if username in users:
        abort(409, message="User already exists with that ID...")


def abort_if_room_not_exists(room_id):
    abort(404, message="Could not find room...")


def abort_if_room_exists(room_id):
    for room in rooms:
        if room_id == room["roomid"]:
            abort(409, message="Room already exists with that ID...")


def abort_if_roomuser_not_exists(room_id):
    abort(404, message=f"Could not find any users for room {room_id}...")


class User(Resource):
    def get(self, username=None):
        if username is None:
            return users, 200
        else:
            abort_if_user_not_exists(username)
            for user in users:
                if user == username:
                    return user, 200

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
            for room in rooms:
                if room_id == room["roomid"]:
                    return room, 200
            abort_if_room_not_exists(room_id)

    def post(self, room_id):
        abort_if_room_exists(room_id)
        room = {"roomid": room_id, "userlist": [], "message_list": []}
        rooms.append(room)
        return room_id, 201


class RoomUser(Resource):

    def get(self, room_id, username=None):
        # room_id is a requirement otherwise client has to request all rooms in Room class
        for room in rooms:
            if room["roomid"] == room_id:
                if username is None:
                    return room["userlist"], 201
                else:
                    for user in room["userlist"]:
                        if user == username:
                            return username + " is in the room " + str(room_id), 201
                    abort(404, message=f"User hasn't been found in room {room_id}...")
        abort(404, message=f"Couldnt find {room_id}...")

        # old code
        # if room_id is None:
        #     # Checks if there are any populated rooms
        #     if len(roomusers) == 0:
        #         abort(404, message="No users in any rooms...")
        #     return roomusers, 200
        #
        # #If specified ID
        # else:
        #     #Checks if room exists
        #     room_exists = False
        #     for room in rooms:
        #         if room_id == room["roomid"]:
        #             room_exists = True
        #     if room_exists == False:
        #         abort_if_room_not_exists(room_id)
        #
        #     #If room exists, return users
        #     #{1 : {users : []}}
        #     if room_id in roomusers:
        #         message = "Users in room number " + str(room_id) + ":"
        #         for user in roomusers[room_id]:
        #             message += user + ", "
        #         return message[:-2], 200
        #     abort_if_roomuser_not_exists(room_id)

    # Tror ikke at vi trenger dette siden vi ikke lagrer en ny rom
    # def post(self, room_id):
    #     #{1 : { users: []}}
    #     #Checks if room exists
    #     if room_id not in rooms:
    #         abort_if_room_not_exists(room_id)
    #
    #     #args = room_user_post_args.parse_args()
    #     if room_id not in roomusers:
    #         roomusers[room_id]["users"] = [args["username"][0]]
    #     else:
    #         roomusers[room_id]["users"].append(args["username"][0])
    #     return args, 201

    def put(self, room_id, username):
        if username not in users:
            abort(404, message=f"Couldnt find user {username}...")

        for room in rooms:
            if room_id == room["roomid"]:
                for username_room in room["userlist"]:
                    if username == username_room:
                        abort(404, message=f"User already connected to the room {room_id}...")
                room["userlist"].append(username)
                return username + " is connected to " + str(room_id), 201
        abort(404, message=f"Couldnt find {room_id}...")


class Message(Resource):
    def get(self, room_id, username):
        for room in rooms:
            if room["roomid"] == room_id:
                for user in room["userlist"]:
                    if user == username:
                        if len(room["message_list"]) == 0:
                            return f"Room {room_id} has no messages.", 201
                        return room["message_list"], 201
                abort(404, message=f"User hasn't been found in room {room_id}...")

    def post(self, room_id, username):
        return

    def put(self, room_id, username, message):
        for room in rooms:
            if room_id == room["roomid"]:
                for username_room in room["userlist"]:
                    if username == username_room:
                        room["message_list"].append(message)
                        return message, 201
                abort(404, message=f"User {username} is not part of room {room_id}...")
        abort(404, message=f"Couldnt find {room_id}...")

#Maybe have only users in the room be able to check the messages

api.add_resource(User, "/api/user/<string:username>", "/api/users")
api.add_resource(Room, "/api/room/<int:room_id>", "/api/rooms")
api.add_resource(RoomUser, "/api/room/<int:room_id>/user/<string:username>", "/api/room/<int:room_id>/users")
api.add_resource(Message, "/api/room/<int:room_id>/user/<string:username>/message/<string:message>", "/api/room/<int:room_id>/user/<string:username>/messages")


@app.route('/')
def index():
    return "SHITTY OBLIG 2"


if __name__ == "__main__":
    app.run(debug=True)
