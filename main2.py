from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

user_post_args = reqparse.RequestParser()
user_post_args.add_argument("username", type=str, help="Username is required...", required=True)
user_post_args.add_argument("usertype", type=str, help="Invalid syntax for usertype...", required=False)

room_post_args = reqparse.RequestParser()
room_post_args.add_argument("room_id", type=int, help="Roomname is required...", required=True)

room_user_post_args = reqparse.RequestParser()
room_user_post_args.add_argument("user_id", type=int, action="append", required=True)

message_post_args = reqparse.RequestParser()
message_post_args.add_argument("message", type=str, help="Message is required...", required=True)

users = {}
rooms = []
roomusers = {}
messages = {}

def abort_if_user_not_exists(user_id):
    if user_id not in users:
        abort(404, message="Could not find user...")

def abort_if_user_exists(user_id):
    if user_id in users:
        abort(409, message="User already exists with that ID...")

def abort_if_room_not_exists(room_id):
    if room_id not in rooms:
        abort(404, message="Could not find room...")

def abort_if_room_exists(room_id):
    for room in rooms:
        if room_id == room["roomid"]:
            abort(409, message="Room already exists with that ID...")


class User(Resource):
    def get(self, user_id=None):
        if user_id is None:
            return users, 200
        else:
            abort_if_user_not_exists(user_id)
            return users[user_id], 200

    def post(self, user_id):
        abort_if_user_exists(user_id)
        args = user_post_args.parse_args()
        users[user_id] = args
        return users[user_id], 201
        
    def delete(self, user_id):
        abort_if_user_not_exists(user_id)
        del users[user_id]
        return '', 204


class Room(Resource):
    def get(self, room_id=None):
        if room_id is None:
            return rooms, 200
        else:
            abort_if_room_not_exists(room_id)
            return rooms[room_id], 200

    def post(self, room_id):
        abort_if_room_exists(room_id)
        room = {"roomid" : room_id, "userlist": [], "message_list": []}
        rooms.append(room)
        return room_id, 201


class RoomUser(Resource):
    def get(self, room_id):
        abort_if_room_not_exists(room_id)
        if not roomusers:
            abort(404, message="No users in any rooms...")
        message = "Users in room number " + str(room_id) + ":"
        for id in roomusers[room_id]["user_id"]:
            message += " "
            message += str(id)
        return message, 200
        
    def post(self, room_id):
        abort_if_room_not_exists(room_id)
        args = room_user_post_args.parse_args()
        if room_id not in roomusers:
            roomusers[room_id] = args
        else:
            roomusers[room_id]["user_id"].append(args["user_id"][0])
        return args, 201


class Message(Resource):
    def get(self, room_id):
        return

    def post(self, room_id, user_id):
        return


api.add_resource(User, "/api/user/<int:user_id>", "/api/users")
api.add_resource(Room, "/api/room/<int:room_id>", "/api/rooms")
api.add_resource(RoomUser, "/api/room/<int:room_id>/users")
#api.add_resource(Message, "/api/room/<int:room_id>/messages", "/api/room/<int:room_id>/<int:user_id>/messages")


@app.route('/')
def index():
    return "SHITTY OBLIG 2"


if __name__ == "__main__":
    app.run(debug=True)