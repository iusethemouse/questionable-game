from app import app, db, login
from hashlib import md5
from datetime import datetime
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), index=True, unique=True)
    name = db.Column(db.String(32))
    #users = db.relationship("User", backref=db.backref('room', lazy=True))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        if self.code:
            return f'<Room {self.name}, code: {self.code}>'
        else:
            return f'<Room {self.name}>'

    def generate_code(self):
        self.code = md5(str(datetime.utcnow()).encode('UTF-8')).hexdigest()[:10]


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), index=True, unique=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship('Room', backref=db.backref('users', lazy=True))
    is_ready = db.Column(db.Boolean, nullable=False)
    score = db.Column(db.Integer)

    def __init__(self, name, room_code):
        r = Room.query.filter_by(code=room_code).first()
        self.room_id = r.id
        self.room = r
        self.name = name
        self.is_ready = False
        self.score = 0

    def __repr__(self):
        return f'<User {self.name}>'