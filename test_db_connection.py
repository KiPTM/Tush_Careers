from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

def test_connection():
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text('SELECT 1'))
            print("Database connection successful")
    except Exception as e:
        print(f"Database connection failed: {e}")

if __name__ == "__main__":
    test_connection()

