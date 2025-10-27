from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    profile_image = db.Column(db.String(100), default='default.jpg')
    user_name = db.Column(db.String(150))
    about = db.Column(db.String())
    profession = db.Column(db.String())
    bio = db.Column(db.String())