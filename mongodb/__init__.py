from pymongo import MongoClient
import utils.config as config

# MongoDB setup
# Connect to the MongoDB server on DigitalOcean
client = MongoClient(config.mongo_db_connection)
# Create (or use existing) database
db = client['conversation_db']

__all__ = [
    db
]