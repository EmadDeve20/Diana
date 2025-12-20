import logging


from langchain.agents.middleware import before_model, AgentState, after_model
from langgraph.runtime import Runtime


@before_model
def log_request_middleware(state:AgentState, runtime: Runtime) -> None:
    logging.info(f"User Request: {state['messages'][-1].content}")

    return None


@after_model
def log_response_middleware(state: AgentState, runtime: Runtime) -> None:
    logging.info(f"Model returned: {state['messages'][-1].content}")

    return None

