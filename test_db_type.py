from app import app, db

with app.app_context():
    print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])
    # Check if you can connect and perform a simple query
    try:
        result = db.session.execute ('SELECT 1')
        print("Database connection successful:", result)
    except Exception as e:
        print("Error:", e)

