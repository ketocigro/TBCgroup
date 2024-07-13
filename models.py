from ext import db, login_manager
from flask_login import UserMixin
from datetime import datetime
class Guitar(db.Model):
    __tablename__ = "guitars"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    img = db.Column(db.String, nullable=False)



class Bass(db.Model):
    __tablename__ = "basses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    img = db.Column(db.String(200), nullable=False)

class Keyboard(db.Model):
    __tablename__ = "keyboards"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    img = db.Column(db.String(200), nullable=False)

class Microphone(db.Model):
    __tablename__ = "microphones"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    img = db.Column(db.String(200), nullable=False)

class Accessory(db.Model):
    __tablename__ = "accessories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    img = db.Column(db.String(200), nullable=False)



class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='User')





@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    product_type = db.Column(db.String, nullable=False)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Card(db.Model):
    __tablename__ = "cards"
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)




class Basket(db.Model):
    __tablename__ = 'basket'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    product_type = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    user = db.relationship('User', backref=db.backref('basket_items', lazy=True))


