#use of flask restful does not need jsonify
#400 = bad request 404= not existed 201 = created successfully 500= internal server error
#filter takes 2 args the lambda func, iterable you add next and None to avoid errors
import secrets
import os
import datetime
from flask import Flask
from db import db
from flask_restful import Api
from flask_jwt import JWT
from security import auth, identity
from api_using_sqlalchemy_section6.resource.user2 import UserRegister
from api_using_sqlalchemy_section6.resource.items2 import Items, ItemResource
from api_using_sqlalchemy_section6.resource.store import StoreResource, Stores


basedir = os.path.abspath(os.path.dirname(__file__))
DB_PASS = os.environ.get('db_pass')
app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = secrets.token_urlsafe(16)
app.config["JWT_EXPIRATION_DELTA"] = datetime.timedelta(seconds=1800)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{DB_PASS}@localhost:5432/api'

#app.config['JWT_AUTH_USERNAME_KEY']='email
jwt = JWT(app, auth, identity)


api.add_resource(ItemResource,'/item/<string:name>')
api.add_resource(Items,"/items")
api.add_resource(UserRegister, "/register")
api.add_resource(StoreResource,"/store/<string:name>")
api.add_resource(Stores, "/stores")


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=4000, debug=True)