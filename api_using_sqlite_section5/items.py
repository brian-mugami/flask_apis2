import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float,
                        required=True,
                        help="Can't be blank")

    @jwt_required()
    def get(self, name):
        item = self.find_an_item(name)
        if item:
            return {"item": {'name': item[0], 'price': item[1]}}, 200
        return {"message": "Item not found"}, 400

    @classmethod
    def find_an_item(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM items WHERE name=?'
        item = cursor.execute(query, (name,))
        row = item.fetchone()

        connection.close()
        if row:
            return {"item": {'name': row[0], 'price': row[1]}}, 200

    @jwt_required()
    def post(self, name):
        if self.find_an_item(name):
            return {name: "already exists"}

        data = Item.parser.parse_args()

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query,(name, data['price']))

        connection.commit()
        connection.close()

        return {"message": "created successfully"}, 201

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        if not self.find_an_item(name):
            create_query = "INSERT INTO items VALUES (?,?)"
            cursor.execute(create_query, (name, data['price']))
            connection.commit()
            connection.close()
            return {name: "created successfully"}
        update_query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(update_query,(name,data["price"]))
        connection.commit()
        connection.close()

        return {name:"updated successfully"}

    @jwt_required()
    def delete(self, name):
        if not self.find_an_item(name):
            return {name: "not found"}
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {name: "deleted"}

class Items(Resource):
    @jwt_required()
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        items = cursor.execute("SELECT * FROM items")
        rows = items.fetchall()

        connection.close()

        return {'items': rows}

