# --------------------------------------------------------------------------------------------
# Title: Performance Review Assistant - General Assistance Workflow
# Author: Tanner Papenfuss
# Date: 2024-05-23
# Description: 
# This workflow is for the user to ask questions, seek advice, or get general assistance 
# related to their performance reviews, goals, and accomplishments. All conversations should 
# be saved and conversations / goals should be retrieved from the mongoDB. This should be 
# another python file that is called by the main orchestrator file. If at any time the user 
# wants to update their goals, they can and will be routed to the CRUD workflow.
# --------------------------------------------------------------------------------------------

# My personal libraries 
from mongodb.insert_conversations import conversation_to_mongo
from utils.conversation import insert_to_history

# Main function to handle the LLM. 
def interactive_llm(user_name, conversation_history, prev_conversations):
    llm_chain = llm_chain
        
    while True:
        # Get user input from the terminal
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            # print("Ending conversation. Here is the convo History: ", conversation_history)
            conversation_to_mongo(user_name, conversation_history)
            break

        try:
            response = llm_chain.invoke({"prev_conversation":prev_conversations, "history": conversation_history, "user_input": user_input})
            print(f"Assistant: {response}")
            conversation_history.append(insert_to_history("User", user_input))
            conversation_history.append(insert_to_history("Assistant", response))
        except Exception as e:
            print(f"Error during LLMChain run: {e}")
