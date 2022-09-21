from api_using_sqlalchemy_section6.db import db

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable= False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, username ,password):
        self.username = username
        self.password = password

    def save_to_db(self):
        #user = User(self._id, self.username, self.password)
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        user = cls.query.filter_by(username=username).first()
        return user

    @classmethod
    def find_by_id(cls, id):
        user = cls.query.filter_by(id=id).first()
        return user