from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from api_using_sqlalchemy_section6.model.item import Item

class ItemResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float,
                        required=True,
                        help="Every item needs a price")
    parser.add_argument('store_id', type=int,
                        required=True,
                        help="Every item needs a store id")

    @jwt_required()
    def get(self, name):
        item = Item.find_an_item(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 400

    @jwt_required()
    def post(self, name):
        data = ItemResource.parser.parse_args()
        item = Item.find_an_item(name)
        if item:
            return {'message': 'item exists'}
        else:
            item = Item(name, **data)
            item.save_to_db()
        return item.json()

    @jwt_required()
    def put(self, name):
        data = ItemResource.parser.parse_args()

        item = Item.find_an_item(name)

        if item is None:
            item = Item(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()

    @jwt_required()
    def delete(self, name):
        item = Item.find_an_item(name)
        if item:
            item.delete_from_db()

        return {item.name: 'deleted successfully'}

class Items(Resource):
    @jwt_required()
    def get(self):
        items = Item.query.all()
        return {'item':[item.json() for item in items]}#list(map(lambda x:x.json,items))
