from app import app, db
from flask_sqlalchemy import SQLAlchemy

def test_get_engine_url():
    with app.app_context():
        # Retrieve and print the SQLAlchemy URL directly
        engine = db.get_engine()
        engine_url = engine.url.render_as_string(hide_password=False).replace('%', '%%')
        print("SQLAlchemy URL:", engine_url)

if __name__ == "__main__":
    test_get_engine_url()

