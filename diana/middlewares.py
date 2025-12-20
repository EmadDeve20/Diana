import logging


from langchain.agents.middleware import before_model, AgentState, after_model
from langchain_core.messages import BaseMessage
from langchain.messages import (
    AIMessage,
    ToolMessage,
    HumanMessage,
    SystemMessage,
) 

from langgraph.runtime import Runtime



def __get_message_type(message:BaseMessage) -> str:
    if isinstance(message, AIMessage):
        return "AI Response"
    elif isinstance(message, HumanMessage):
        return "User Request"
    elif isinstance(message, ToolMessage):
        return "Tool Response"
    elif isinstance(message, SystemMessage):
        return "System Message"
    else:
        return "Unknown"


@before_model
def log_request_middleware(state:AgentState, runtime: Runtime) -> None:
    message_type = __get_message_type(state['messages'][-1]) 

    logging.info(f"{message_type}: {state['messages'][-1].content}")

    return None


@after_model
def log_response_middleware(state: AgentState, runtime: Runtime) -> None:
    message_type = __get_message_type(state['messages'][-1]) 

    logging.info(f"{message_type}: {state['messages'][-1].content}")

    return None

