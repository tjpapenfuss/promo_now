# query_conversations.py

from pymongo import MongoClient
import config

# Connect to the MongoDB server on DigitalOcean
client = MongoClient(config.mongo_db_connection)

# Access the database
db = client['conversation_db']

# Access the collection
collection = db['conversations']

# Find all conversations for a specific user
user_id = "tpap"
conversations = collection.find({"metadata.user_id": user_id})

# Display the conversations
for conv in conversations:
    print(conv)

print("Query complete.")