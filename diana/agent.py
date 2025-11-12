from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain.agents.factory import create_agent

from diana.settings import (
    HUGGINGFACE_KEY,
    TEMPERATURE,
    MODEL,
    SYSTEM_PROMPT
)

from diana.ai_tools import TOOLS

chat_endpoint = HuggingFaceEndpoint(
    model=MODEL,
    temperature=TEMPERATURE,
    huggingfacehub_api_token=HUGGINGFACE_KEY
)

chat_model = ChatHuggingFace(llm=chat_endpoint)

# TODO: Check this is ok or not? maybe we need to use react agent
# TODO: Add Memeory
agent = create_agent(
    model=chat_model,
    tools=TOOLS,
    system_prompt=SYSTEM_PROMPT
)

