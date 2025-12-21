from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain.agents.factory import create_agent
from langchain.agents.middleware import (
    TodoListMiddleware,
    LLMToolSelectorMiddleware,
)
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
    AIMessage,
    ToolMessage
)

from langgraph.graph import MessagesState
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver



from diana.settings import settings
from diana.middlewares import (
    log_request_middleware,
    log_response_middleware,
)
from diana.ai_tools import TOOLS


chat_endpoint = HuggingFaceEndpoint(
    model=settings.MODEL,
    temperature=settings.TEMPERATURE,
    huggingfacehub_api_token=settings.HUGGINGFACE_KEY
)

chat_model = ChatHuggingFace(llm=chat_endpoint)


# TODO: research for best practice to use agent with memory
# maybe it is better to make our agent before like builder.
# I mean before compile, and then compile our graph in this function 
async def run_agent(thread_id:int,
message:HumanMessage|AIMessage|ToolMessage|SystemMessage) -> MessagesState:
    """
    talk with your agent or execute agent

    Args:
        thread_id (int): thread id
        human_message (str): message of human

    Returns:
        MessagesState: return MessagesState
    """

    config = {"configurable": {"thread_id": thread_id}}

    async with AsyncSqliteSaver.from_conn_string(settings.AI_MEMORY_DB) as checkpointer:

        agent = create_agent(
            model=chat_model,
            tools=TOOLS,
            system_prompt=settings.SYSTEM_PROMPT,
            checkpointer=checkpointer,
            middleware=[log_request_middleware,
                        log_response_middleware,
                        TodoListMiddleware(),
                        LLMToolSelectorMiddleware(
                            model=chat_model.name,
                            max_tools=10,
                        )]
        )

        res = await agent.ainvoke({"messages": message}, config=config)

        return res
