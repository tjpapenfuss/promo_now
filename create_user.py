# create_user.py

from pymongo import MongoClient
import config

# Connect to the MongoDB server on DigitalOcean
client = MongoClient(config.mongo_db_connection)

# Create (or use existing) database
db = client['conversation_db']

# Create (or use existing) collection for users
user_collection = db['users']

# Function to create a new user
def create_user(user_id, name, email):
    # Check if the user already exists
    existing_user = user_collection.find_one({"user_id": user_id})
    if existing_user:
        print(f"User with ID {user_id} already exists.")
        return
    
    # Create a new user document
    user = {
        "user_id": user_id,
        "name": name,
        "email": email
    }
    
    # Insert the new user into the collection
    user_collection.insert_one(user)
    print(f"User {name} created successfully.")

# Example usage
if __name__ == "__main__":
    # Example user data
    user_id = "tpap"
    name = "Tanner Papenfuss"
    email = "tpap@gmail.com"
    
    # Create the new user
    create_user(user_id, name, email)