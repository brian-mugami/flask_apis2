#use of flask restful does not need jsonify
#400 = bad request 404= not existed 201 = created successfully 500= internal server error
#filter takes 2 args the lambda func, iterable you add next and None to avoid errors
import secrets
import datetime
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import auth, identity
from user import UserRegister
from items import Items,Item

app = Flask(__name__)
api = Api(app)
app.secret_key = secrets.token_urlsafe(16)
app.config["JWT_EXPIRATION_DELTA"] = datetime.timedelta(seconds=1800)
#app.config['JWT_AUTH_USERNAME_KEY']='email
jwt = JWT(app, auth, identity)


api.add_resource(Item,'/item/<string:name>')
api.add_resource(Items,"/items")
api.add_resource(UserRegister, "/register")


if __name__ == '__main__':
    app.run(port=2000, debug=True)