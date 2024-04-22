from config import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email_id = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(20))
    add_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, username, email_id, address ):
        self.username = username
        self.email_id = email_id
        self.address = address


class Wall(db.Model):
    __tablename__ = 'Wall'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)  # Define the ForeignKey constraint here
    admin = db.Column(db.String(50))
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    add_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('wall', lazy=True))

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'admin': self.admin,
            'title': self.title,
            'description': self.description,
            'add_on': self.add_on.isoformat()  # Assuming add_on is a datetime object
        }


