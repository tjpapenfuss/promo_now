# from langchain import LLMChain
from datetime import datetime, timezone

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
