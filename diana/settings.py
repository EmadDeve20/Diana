from typing import Optional

import logging

from dotenv import load_dotenv

from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):


    TELEGRAM_TOKEN : str

    PROXY_URL : Optional[str]

    HUGGINGFACE_KEY : Optional[str] = Field(None)
    OPENAI_API_KEY : Optional[str] = Field(None)
    ANTHROPIC_API_KEY: Optional[str] = Field(None)
    GOOGLE_API_KEY: Optional[str] = Field(None)
    GROQ_API_KEY: Optional[str] = Field(None)
    OPENROUTER_API_KEY: Optional[str] = Field(None) 


    MODEL : str 

    TEMPERATURE : float = Field(0.0)

    SYSTEM_PROMPT : str 

    OWNER_USERNAME : str 

    AI_MEMORY_DB : str = Field("checkpoints.sqlite")

    DB_USER : str
    DB_PASSWORD : str
    DB_HOST : str
    DB_PORT : str
    DB_NAME : str

    DEBUG:bool = Field(True)


settings = Settings()

logging.basicConfig(level=logging.DEBUG if settings.DEBUG else logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')



