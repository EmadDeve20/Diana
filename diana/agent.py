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
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.chat_models import init_chat_model
 
from langgraph.graph import MessagesState
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver


from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq



from diana.settings import settings, logging
from diana.middlewares import (
    log_request_middleware,
    log_response_middleware,
)
from diana.ai_tools import TOOLS
from diana.common import Borg


def generate_model() -> BaseChatModel:
    """
    generate model from AI's provider key in .env file 

    Raises:
        ValueError: raise ValueError if there is not any key for AI's provider

    Returns:
        BaseChatModel: return generated chat model

    """

    if settings.HUGGINGFACE_KEY:

        logging.info("generating model from huggingface ... ")

        chat_endpoint = HuggingFaceEndpoint(
            model=settings.MODEL,
            temperature=settings.TEMPERATURE,
            huggingfacehub_api_token=settings.HUGGINGFACE_KEY
        )

        return ChatHuggingFace(llm=chat_endpoint)
    
    if settings.OPENAI_API_KEY:
        logging.info("generating model from openAI ... ")

        return ChatOpenAI(
                   model=settings.MODEL,
                   temperature=settings.TEMPERATURE)


    if settings.ANTHROPIC_API_KEY:
        logging.info("generating model from Anthropic ... ")

        return ChatAnthropic(
            model_name=settings.MODEL,
            temperature=settings.TEMPERATURE,
            timeout=None,
            stop=None
        )
    
    if settings.GOOGLE_API_KEY:
        logging.info("generating model from GoogleAI ... ")

        return ChatGoogleGenerativeAI(
            model=settings.MODEL,
            temperature=settings.TEMPERATURE,
            max_tokens=None,
            timeout=None,
            max_retries=2
        )
    
    if settings.GROQ_API_KEY:
        logging.info("generating model from Groq ... ")

        return ChatGroq(
            model=settings.MODEL,
            temperature=settings.TEMPERATURE,
            max_tokens=None,
            reasoning_format="parsed",
            timeout=None,
            max_retries=2,
        )
    
    if settings.OPENROUTER_API_KEY:
        logging.info("generating model from OpenRouter")

        return init_chat_model(
            model=settings.MODEL,
            model_provider="openai",
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.OPENROUTER_API_KEY
        )


    raise ValueError("There's no API key for the AI provider.")



class Agent(Borg):

    def __init__(self, model:BaseChatModel|None=None):
        super().__init__()

        if model and not hasattr(self, "model"):
            self.model = model

        elif model is None and not hasattr(self, "model"):
            self.model = generate_model()


    async def run_agent(self, thread_id:int,
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
                model=self.model,
                tools=TOOLS,
                system_prompt=settings.SYSTEM_PROMPT,
                checkpointer=checkpointer,
                middleware=[log_request_middleware,
                            log_response_middleware,
                            TodoListMiddleware(),
                            LLMToolSelectorMiddleware(
                                model=self.model.name,
                                max_tools=10,
                            )]
            )

            res = await agent.ainvoke({"messages": message}, config=config)

            return res
