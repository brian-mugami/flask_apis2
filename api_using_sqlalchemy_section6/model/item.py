from api_using_sqlalchemy_section6.db import db


class Item(db.Model):

    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable= False)
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price':self.price, 'store': self.store_id}

    @classmethod
    def find_an_item(cls, name):
        return cls.query.filter_by(name=name).first() #select * from items where name=name..cls instead of item

    #@classmethod it is using the item class..makes more sense to make it a self
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    #@classmethod
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()