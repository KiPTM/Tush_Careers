# models.py
from extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Integer, nullable=False)

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'location': self.location,
            'salary': self.salary
        }

    def __repr__(self):
        return f"Job('{self.title}', '{self.location}', '{self.salary}')"


