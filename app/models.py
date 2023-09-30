from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
 
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    
    reading_list = db.relationship("Book", backref="reader")

    def __init__(self, email, password):
        self.email = email
        self.hash_password(password)

    def hash_password(self, password):
        self.password = generate_password_hash(password) 

    def check_password(self, password):
        return check_password_hash(self.password, password)
        
    def save(self):
        db.session.add(self)
        db.session.commit()

        
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    
    def __init__(self, name, author, user_id):
        self.name = name
        self.author = author
        self.user_id = user_id
        
    def save(self):
        db.session.add(self)
        db.session.commit()