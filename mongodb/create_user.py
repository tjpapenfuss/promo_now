# create_user.py
import uuid
from mongodb import users_db

# Create (or use existing) collection for users
user_collection = users_db['users']

def get_user_info(user_name):
    return user_collection.find_one({"user_name": user_name})

def get_user_id(user_name):
    existing_user = user_collection.find_one({"user_name": user_name})
    if existing_user:
        return existing_user['user_id']
    print(f"Username {user_name} doesn't exist.")
    return 

def get_user_name(user_id):
    existing_user = user_collection.find_one({"user_id": user_id})
    if existing_user:
        return existing_user['user_name']
    print(f"User ID {user_id} doesn't exist.")
    return 

# Function to create a new user
def create_user(user_name, name, email):
    # Check if the user already exists
    existing_user = user_collection.find_one({"user_name": user_name})
    if existing_user:
        print(f"User with ID {user_name} already exists.")
        return
    
    # Create a new user document
    user = {
        "user_id": str(uuid.uuid4()), # make a random UUID for the user's unique ID. 
        "user_name": user_name,
        "name": name,
        "email": email
    }
    
    # Insert the new user into the collection
    user_collection.insert_one(user)
    print(f"User {name} created successfully.")

# Example usage
if __name__ == "__main__":
    # Example user data
    user_name = "tpap"
    name = "Tanner Papenfuss"
    email = "tpap@gmail.com"
    
    # Create the new user
    create_user(user_name, name, email)