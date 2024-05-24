from datetime import datetime, timezone

# Internal package imports
from mongodb.create_user import create_user, get_user_info
from mongodb.query_conversations import get_conversations, format_conversations

def insert_to_history(sender, message):
    return {
                "sender": f"{sender}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "message": f"{message}"
            }

def initialize_conversation_history(user_name):
    previous_conversations = get_conversations(user_name)
    return format_conversations(previous_conversations)

def initialize_conversation():
    # Ask for username
    user_name = input("Assistant: Please enter your username: \nYou: ")
    conversation_history = []
    prev_conversations = ""
    # Check if user exists
    user_info = get_user_info(user_name)
    if user_info:
        print(f"Assistant: Welcome back, {user_info['name']}!")
        prev_conversations = initialize_conversation_history(user_name)
    else:
        print("Assistant: I don't have a record of your username.")
        name = input("Assistant: Please enter your name: \nYou: ")
        email = input("Assistant: Please enter your email: \nYou: ")
        create_user(user_name, name, email)
        print(f"Assistant: Nice to meet you, {name}! Let's start a new conversation.")
        conversation_history.append(insert_to_history("User", f"My name is {name}"))
        conversation_history.append(insert_to_history("Assistant", f"Hey {user_name}, tell me about your day."))        
    return user_name, conversation_history, prev_conversations