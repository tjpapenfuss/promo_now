import utils.config as config
import os
from langchain_openai import OpenAI

# Set your OpenAI API key here
os.environ["OPENAI_API_KEY"] = config.api_key

def get_openai_llm():
    """Initialize and return the OpenAI model."""
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

