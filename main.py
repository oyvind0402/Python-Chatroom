from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

user_post_args = reqparse.RequestParser()
# user_post_args.add_argument("userid", type=str, help="Userid is required...", required=True)
# user_post_args.add_argument("usertype", type=str, help="Invalid syntax for usertype...", required=False)

room_post_args = reqparse.RequestParser()
room_post_args.add_argument("roomname", type=str, help="Roomname is required...", required=True)
# room_post_args.add_argument("room_users", type=str,
# help="Invalid syntax for adding a user to the room...", required=False, action="append")
room_get_args = reqparse.RequestParser()
room_get_args.add_argument("roomid", type=str, help="Roomname is required...", required=True)
room_put_args = reqparse.RequestParser()
room_put_args.add_argument("roomid", type=str, help="Roomname is required...", required=True)
room_put_args.add_argument("user_id", type=str, help="User ID is required...", required=True)

# room_user_post_args = reqparse.RequestParser()
# room_user_post_args.add_argument("user_id", type=str, help="User id is required...", required=True)
# room_user_post_args.add_argument("username", type=str, help="Username is required...", required=True)

users = []
rooms = []
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
    if room_id in rooms:
        abort(409, message="Room already exists with that ID...")


class User(Resource):
    def get(self, user_id=None):
        if user_id is None:
            return users, 200
        else:
            abort_if_user_not_exists(user_id)
            return users[user_id], 200

    # def post(self, user_id):
    #    abort_if_user_exists(user_id)
    #    args = user_post_args.parse_args()
    #    users[user_id] = args
    #    return users[user_id], 201

    def post(self, user_id):
        abort_if_user_exists(user_id)
        # args = user_post_args.parse.args()
        users.append(user_id)
        return user_id, 201

    def delete(self, user_id):
        abort_if_user_not_exists(user_id)
        del users[user_id]
        return '', 204


class Room(Resource):
    user_list = []

    def get(self, room_name):
        if room_name is None:
            return 404
        else:
            abort_if_room_not_exists(room_name)
            return room_name, 200

    def post(self, room_name):
        abort_if_room_exists(room_name)
        rooms.append(room_name)
        # abort_if_room_exists(room_id)
        # args = room_post_args.parse_args()
        # rooms[room_id] = args

        return room_name, 201

    def put(self, room_name, user_id):
        args = room_post_args.parse_args()

    def adduser(self, username):
        user_list.append

class Rooms(Resource):
    def get(self):
        return rooms, 200


"""""
class RoomUser(Resource):
    def get(self, room_id):
        return rooms[room_id]["room_users"]

    def post(self, room_name):
        args = room_user_post_args()
        rooms[room_id]["room_users"] = args
        return rooms[room_id]["room_users"], 201
"""""

# class Message(Resource):
#     def get(self, room_id):
#         return

# def post(self, room_id, user_id):
#     return


api.add_resource(User, "/api/user/<string:user_id>", "/api/users")
api.add_resource(Room, "/api/room/<string:room_name>")
api.add_resource(Rooms, "/api/rooms")


# api.add_resource(RoomUser, "/api/room/<int:room_id>/users")


# api.add_resource(Message, "/api/room/<int:room_id>/messages")
# api.add_resource(Message, "/api/room/<int:room_id>/<int:user_id>/messages")


@app.route('/')
def index():
    return "SHITTY OBLIG 2"


if __name__ == "__main__":
    app.run(debug=True)
