from api_using_sqlalchemy_section6.db import db

class Store(db.Model):

    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable= False)
    items = db.relationship('Item', backref='stores', lazy='dynamic')#lazy=dynamic converts this from calling self.items to using a query builder

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}#self.items isused if lazy is not dynamic

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