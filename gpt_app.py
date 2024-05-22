from langchain import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from pymongo import MongoClient
import os

import config

# Set your OpenAI API key here
os.environ["OPENAI_API_KEY"] = config.api_key

def get_openai_llm():
    """Initialize and return the OpenAI model."""
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_prompt_template():
    """Create and return the prompt template."""
    template = """
    You are a helpful assistant. You are trying to help the user to organize their goals into alignment goals and delivering results goals. 

    Conversation history:
    {history}

    User: {user_input}

    Assistant:
    """
    return PromptTemplate(input_variables=["history", "user_input"], template=template)

def initialize_conversation():
    """Initialize the conversation with a greeting."""
    user_name = input("Assistant: Hey, what's your name? \nYou: ")
    conversation_history = f"User: My name is {user_name}\nAssistant: Hey {user_name}, tell me about your day."
    print(f"Assistant: Hey {user_name}, tell me about your day.")
    return user_name, conversation_history

def interactive_llm():
    """Run the interactive language model."""
    llm = get_openai_llm()
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
    
    user_name, conversation_history = initialize_conversation()

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Ending conversation.")
            break

        try:
            response = llm_chain.invoke({"history": conversation_history, "user_input": user_input})
            print(f"Assistant: {response}")
            conversation_history += f"\nUser: {user_input}\nAssistant: {response}"
        except Exception as e:
            print(f"Error during LLMChain run: {e}")

if __name__ == "__main__":
    interactive_llm()
