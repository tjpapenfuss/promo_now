#### NEED TO CLEAN THIS UP #####

import os
from langchain_core.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain

# Set your OpenAI API key here
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

# Initialize the OpenAI model
def get_openai_llm():
    """Initialize and return the OpenAI model."""
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Import workflow modules
import mongodb
import mongodb.insert_conversations
from mongodb.create_user import create_user, get_user_info
from utils.prompt_templates import create_prompt_template
from mongodb.query_conversations import get_conversations, format_conversations
import utils.config as config

# Initialize LLM and prompt template
llm = get_openai_llm()
prompt_template = create_prompt_template()

# Verify that both llm and prompt_template are initialized correctly
if llm is None or prompt_template is None:
    print("Error initializing the LLM or Prompt Template.")
else:
    try:
        llm_chain = prompt_template | llm
    except Exception as e:
        print(f"Error initializing LLMChain: {e}")
        llm_chain = None

# Exported objects
__all__ = [
    "client", "db", "users_collection", "get_openai_llm", "create_prompt_template", 
    "handle_crud_workflow", "general_assistance", "list_activities", "summarize_achievements", 
    "provide_tips", "start_guidance_workflow", "llm_chain"
]
