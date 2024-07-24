from extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    applications = db.relationship('JobApplication', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    applications = db.relationship('JobApplication', backref='job', lazy=True)

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'location': self.location,
            'salary': self.salary
        }

    def __repr__(self):
        return f"Job('{self.title}', '{self.location}', '{self.salary}')"

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    applied_on = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f"Application(User ID: {self.user_id}, Job ID: {self.job_id}, Date: {self.applied_on})"

