from workflows.gpt_app import interactive_llm
from utils.initialize_conversation import initialize_conversation


if __name__ == "__main__":
    # Call LLM
    user_name, conversation_history, prev_conversations = initialize_conversation()
    interactive_llm(user_name, conversation_history, prev_conversations)