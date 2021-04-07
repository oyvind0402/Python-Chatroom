from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

user_post_args = reqparse.RequestParser()
user_post_args.add_argument("username", type=str, help="Username is required...", required=True)
user_post_args.add_argument("usertype", type=str, help="Invalid syntax for usertype...", required=False)

room_post_args = reqparse.RequestParser()
room_post_args.add_argument("roomname", type=str, help="Roomname is required...", required=True)
#room_post_args.add_argument("room_users", type=str, help="Invalid syntax for adding a user to the room...", required=False, action="append")

room_user_post_args = reqparse.RequestParser()
room_user_post_args.add_argument("user_id", type=str, help="User id is required...", required=True)
room_user_post_args.add_argument("username", type=str, help="Username is required...", required=True)

users = {}
rooms = {}
messages = {}


class User(Resource):
    def get(self, user_id):
        return users[user_id], 200

    def post(self, user_id):
        args = user_post_args.parse_args()
        users[user_id] = args
        return users[user_id], 201
        
    def delete(self, user_id):
        del users[user_id]
        return '', 204


class Room(Resource):
    def get(self, room_id):
        return rooms[room_id], 200

    def post(self, room_id):
        args = room_post_args.parse_args()
        rooms[room_id] = args
        return rooms[room_id], 201


class RoomUser(Resource):
    def get(self, room_id):
        return rooms[room_id]["room_users"]
    def post(self, room_id):
        args = room_user_post_args()
        rooms[room_id]["room_users"] = args
        return rooms[room_id]["room_users"], 201


# class Message(Resource):
#     def get(self, room_id):
#         return

    # def post(self, room_id, user_id):
    #     return


api.add_resource(User, "/api/user/<int:user_id>")
api.add_resource(Room, "/api/rooms", "/api/room/<int:room_id>")
api.add_resource(RoomUser, "/api/room/<int:room_id>/users")
#api.add_resource(Message, "/api/room/<int:room_id>/messages")
#api.add_resource(Message, "/api/room/<int:room_id>/<int:user_id>/messages")


@app.route('/')
def index():
    return "SHITTY OBLIG 2"

@app.route('/api/users')
def get_users():
    return users

@app.route('/api/rooms')
def get_rooms():
    return rooms


if __name__ == "__main__":
    app.run(debug=True)