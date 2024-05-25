from mongodb import conversation_db
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

    # Create (or use existing) collection
    collection = conversation_db['conversations']

    # make a random UUID
    conversation_id = str(uuid.uuid4())

    # Insert the conversation into the collection
    collection.insert_one(generate_conversation_json(conversation_id, user_name, messages))

    # Create an index on the metadata.user_name field
    collection.create_index(user_name)

    print("Conversation inserted and index created.")

