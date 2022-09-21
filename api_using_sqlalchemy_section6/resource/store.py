from flask_restful import Resource,reqparse
from api_using_sqlalchemy_section6.model.stores import Store

class StoreResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, type=str, help='Input new store name')


    def get(self, name):
        store = Store.find_an_item(name)
        if store:
            return store.json()
        return {'message': "store not found"}, 404


    def post(self, name):
        old_store = Store.find_an_item(name)
        if old_store:
            return {"message": "store already exists"}
        store = Store(name)
        try:
            store.save_to_db()
        except:
            return {"message": "an error occured"}, 500
        return store.json()


    def delete(self, name):
        store = Store.find_an_item(name)
        store.delete_from_db()
        return {name: 'deleted'}

    def put(self,name):
        data = self.parser.parse_args()
        store = Store.find_an_item(name)
        if store:
            store.name = data['name']
            store.save_to_db()
            return store.json()
        else:
            new_store = Store(data['name'])
            new_store.save_to_db()
            return new_store.json()

class Stores(Resource):
    def get(self):
        stores = Store.query.all()
        return {'stores': [store.json() for store in stores]}

