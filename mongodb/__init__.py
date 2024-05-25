from pymongo import MongoClient
import utils.config as config
import mongodb.config

# MongoDB setup
# Connect to the MongoDB server on DigitalOcean
client = MongoClient(config.mongo_db_connection)
# Create (or use existing) database
conversation_db = client['conversation_db']

users_db = client['users']

__all__ = [
    conversation_db, users_db
]