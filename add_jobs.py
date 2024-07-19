from app import app, db
from models import Job

# Create some job entries
jobs = [
    Job(title="Software Developer", location="New York", salary=80000),
    Job(title="Data Scientist", location="San Francisco", salary=120000),
    Job(title="Product Manager", location="Austin", salary=100000),
    Job(title="UX Designer", location="Los Angeles", salary=90000),
]

with app.app_context():
    db.create_all()  # Create tables if they don't exist
    for job in jobs:
        db.session.add(job)
    db.session.commit()

print("Jobs added successfully!")
