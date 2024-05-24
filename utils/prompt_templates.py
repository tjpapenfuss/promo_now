from langchain_core.prompts import PromptTemplate

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

def basic_prompt_template():
    # Define your prompt template
    template = """
    You are a helpful assistant. You are trying to help the user to organize their goals into alignment goals and 
    delivering results goals.

    Conversation history:
    {history}

    User: {user_input}

    Assistant:
    """

    # Create a PromptTemplate instance
    return PromptTemplate(input_variables=["prev_conversation", "history", "user_input"], template=template)
