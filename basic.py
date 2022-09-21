#use of flask restful does not need jsonify
#400 = bad request 404= not existed 201 = created successfully
#filter takes 2 args the lambda func, iterable you add next and None to avoid errors
import secrets

from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_jwt import JWT, jwt_required
from security import auth,identity

main = Flask(__name__)
api = Api(main)
main.secret_key = secrets.token_urlsafe(16)

jwt = JWT(main, auth, identity)

items = []

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float,
                        required=True,
                        help="Can't be blank")

    @jwt_required()
    def get(self, name):
        #for item in items:
            #if item['name'] == name:
                #return item
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {"item": item}, 200 if item else 404

    @jwt_required()
    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': f"item {name} exists"}, 400

        #request_data = request.get_json(silent=True)#force=True

        data = Item.parser.parse_args()
        item = {'name': name,
                'price': data['price']}
        items.append(item)
        return item, 201

    @jwt_required()
    def put(self,name):
        #data = request.get_json()
        data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item:
            item.update(data)#update is in dicts
        new_item = {'name': name, 'price':data['price']}
        items.append(new_item)
        return {'item added': new_item}


    @jwt_required()
    def delete(self,name):
        global items
        #for item in items:
            #if item['name'] == name:
                #return item
        items = list(filter(lambda x:x['name'] != name,items))
        return {"message": "item deleted"}

class Items(Resource):
    def get(self):
        return {"item": items}

api.add_resource(Item,'/item/<string:name>')
api.add_resource(Items,"/items")


if __name__ == '__main__':
    main.run(port=1000, debug=True)