from pymongo import MongoClient
import json
import config
from datetime import datetime, timezone
import uuid


def generate_conversation_json(conversation_id, user_name, messages):
    conversation_json = {
        "conversation_id": conversation_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "messages": messages,
        "metadata": {
            "user_name": user_name,
            "language": "en",
            "context": {}
        }
    }
    return conversation_json

def conversation_to_mongo(user_name, messages):

    # Connect to the MongoDB server on DigitalOcean
    client = MongoClient(config.mongo_db_connection)

    # Create (or use existing) database
    db = client['conversation_db']

    # Create (or use existing) collection
    collection = db['conversations']

    # make a random UUID
    conversation_id = str(uuid.uuid4())

    #generate JSON
    json = generate_conversation_json(conversation_id, user_name, messages)
    print(json)

    # Insert the conversation into the collection
    collection.insert_one(generate_conversation_json(conversation_id, user_name, messages))

    # Create an index on the metadata.user_name field
    collection.create_index(user_name)

    print("Conversation inserted and index created.")



# Legacy
# Opening JSON file
# f = open('./utils/sample_conversation.json')
 
# returns JSON object as 
# a dictionary
# conversation = json.load(f)

# # Sample JSON conversation data
# conversation_data = 

# # Load JSON data
# conversation = json.loads(utils/sample)



