from workflows.gpt_app import interactive_llm
from utils.conversation import initialize_conversation

# Delete later
from mongodb.create_user import get_user_id
from mongodb.insert_goals import delete_goal, list_goals
# create_user("jorbear", "jor", "ffds@gmail.com")
# print(get_user_id("jorbear"))

if __name__ == "__main__":
    # Call LLM
    user_name, conversation_history, prev_conversations = initialize_conversation()
    interactive_llm(user_name, conversation_history, prev_conversations)

    #delete_goal(get_user_id("tpap"), "1")