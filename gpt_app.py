# from langchain import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from pymongo import MongoClient
import os
from datetime import datetime, timezone

# My personal libraries 
import insert_conversations
from create_user import create_user, get_user_info
from query_conversations import get_conversations, format_conversations
import config

# Set your OpenAI API key here
os.environ["OPENAI_API_KEY"] = config.api_key

def get_openai_llm():
    """Initialize and return the OpenAI model."""
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def initialize_conversation_history(user_name):
    previous_conversations = get_conversations(user_name)
    return format_conversations(previous_conversations)

def create_prompt_template():
    # Define your prompt template
    template = """
    You are a helpful assistant. You are trying to help the user to organize their goals into alignment goals and 
    delivering results goals. 

    Previous Conversations:
    {prev_conversation}

    Conversation history:
    {history}

    User: {user_input}

    Assistant:
    """

    # Create a PromptTemplate instance
    return PromptTemplate(input_variables=["prev_conversation", "history", "user_input"], template=template)

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
        conversation_history.append(
        {
            "sender": "User",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": f"My name is {name}"
        })
        conversation_history.append(
        {
            "sender": "Assistant",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": f"Hey {user_name}, tell me about your day."
        })
    return user_name, conversation_history, prev_conversations

# Main function to handle the LLM. 
def interactive_llm():
    # Initialize the OpenAI model
    llm = get_openai_llm()

    # Create the prompt template
    prompt_template = create_prompt_template()
    
    # Verify that both llm and prompt_template are initialized correctly
    if llm is None or prompt_template is None:
        print("Error initializing the LLM or Prompt Template.")
        return

    try:
        llm_chain = prompt_template | llm
    except Exception as e:
        print(f"Error initializing LLMChain: {e}")
        return
    
    user_name, conversation_history, prev_conversations = initialize_conversation()
    
    while True:
        # Get user input from the terminal
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            # print("Ending conversation. Here is the convo History: ", conversation_history)
            insert_conversations.conversation_to_mongo(user_name, conversation_history)
            break

        try:
            response = llm_chain.invoke({"prev_conversation":prev_conversations, "history": conversation_history, "user_input": user_input})
            print(f"Assistant: {response}")
            conversation_history.append(
            {
                "sender": "User",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "message": f"{user_input}"
            })
            conversation_history.append(
            {
                "sender": "Assistant",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "message": f"{response}"
            })
        except Exception as e:
            print(f"Error during LLMChain run: {e}")

if __name__ == "__main__":
    # Call LLM
    interactive_llm()