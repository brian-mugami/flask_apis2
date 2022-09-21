import sqlite3
from flask_restful import Resource, reqparse

class User:
    def __init__(self, _id, username,password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        select_query = 'SELECT * FROM users WHERE username=?'
        result = cursor.execute(select_query, (username,))#parameters have always to be tuples
        row = result.fetchone()
        if row:
            user = cls(*row) #row[0], row[1], row[2]
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        connection.close()
        if row:
            user = cls(*row)
        #else:
         #   user = None
            return user

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="Username Required")
    parser.add_argument("password", type=str, required=True, help="Password Required")

    def post(self):
        data = UserRegister.parser.parse_args()
        if User.find_by_username(data['username']):#before creating connection
            return {"message": "invalid/already exists"}, 400
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        insert_query = "INSERT INTO users VALUES(NULL,?,?)"

        cursor.execute(insert_query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "user created successfully"}, 201