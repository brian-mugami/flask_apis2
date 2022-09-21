from flask_restful import Resource, reqparse
from api_using_sqlalchemy_section6.model.user import User

class UserRegister(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument("username", type=str, required=True, help="Username Required")
    parser.add_argument("password", type=str, required=True, help="Password Required")

    def post(self):
        data = UserRegister.parser.parse_args()
        if User.find_by_username(data['username']):#before creating connection
            return {"message": "invalid/already exists"}, 400

        user = User(**data)
        user.save_to_db()

        return {"message": "user created successfully"}, 201