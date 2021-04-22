import sqlite3
from flask_restful import Resource, reqparse
from models.user_model import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, help="This field can not be blank")
    parser.add_argument('password', type=str, help="This field can not be blank")

    def post(self):
        data = UserRegister.parser.parse_args()
        user = UserModel(data['username'], data['password'])
        # user_exists = User.find_by_username(data['username'])

        if UserModel.find_by_username(data['username']):
            return {'message': "User already exists"}, 400

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "INSERT INTO users VALUES (NULL, ?, ?)"
        # cursor.execute(query, (data['username'], data['password'],))
        #
        # connection.commit()
        # connection.close()
        user.save_to_db()

        return {'message': "User is created successfully"}, 201
