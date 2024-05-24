from utils.prompt_templates import create_prompt_template
from utils.setup_openai import get_openai_llm

# Initialize the OpenAI model
llm = get_openai_llm()

# Create the prompt template
prompt_template = create_prompt_template()

# Verify that both llm and prompt_template are initialized correctly
if llm is None or prompt_template is None:
    print("Error initializing the LLM or Prompt Template.")

try:
    llm_chain = prompt_template | llm
except Exception as e:
    print(f"Error initializing LLMChain: {e}")

__all__ = [
    llm_chain, prompt_template, llm
]