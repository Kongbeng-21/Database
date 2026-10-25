from pymongo import MongoClient

def get_db():
    try:
        # --- Task: Database Connection ---
        # Connect to MongoDB (user/password must match docker-compose.yml)
        client = MongoClient("mongodb://root:kongbeng@localhost:27017/")

        # Select the 'instagram_db' database assignment
        db = client['instagram_db']
        
        # Return the database object to be used by the Flask application
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None