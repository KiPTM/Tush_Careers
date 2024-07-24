import sqlite3

def inspect_db(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get a list of all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("Tables in the database:")
        for table in tables:
            print(table[0])
            
            # Print the schema of each table
            cursor.execute(f"PRAGMA table_info({table[0]})")
            schema = cursor.fetchall()
            for column in schema:
                print(f" - {column[1]}: {column[2]}")
            
            # Optionally, print the first few rows of each table
            cursor.execute(f"SELECT * FROM {table[0]} LIMIT 5")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        
        conn.close()
    except sqlite3.Error as e:
        print(f"Error inspecting database: {e}")

# Inspect the site.db file
inspect_db('site.db')  # Adjust the path if site.db is located elsewhere

