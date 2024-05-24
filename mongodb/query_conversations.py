# query_conversations.py

from mongodb import db
import config

# Access the collection
collection = db['conversations']

def get_conversations(user_name):
    # Find all conversations for a specific user
    conversations = collection.find({"metadata.user_name": user_name})
    return list(conversations)

def format_conversations(conversations):
    formatted = ""
    for conv in conversations:
        for message in conv["messages"]:
            sender = "User" if message["sender"] == "User" else "Assistant"
            formatted += f"{sender}: {message['message']}\n"
    return formatted

if __name__ == "__main__":
    user_name = "tpap"
    conversations = get_conversations(user_name)
    formatted_conversations = format_conversations(conversations)
    
    # Display the formatted conversations
    print(formatted_conversations)

    print("Query complete.")