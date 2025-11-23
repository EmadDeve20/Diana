
import logging

from dotenv import load_dotenv

from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):


    TELEGRAM_TOKEN : str

    PROXY_URL : str | None

    HUGGINGFACE_KEY : str | None = Field(None)

    MODEL : str 

    TEMPERATURE : float = Field(0.0)

    SYSTEM_PROMPT : str 

    OWNER_USERNAME : str 

    AI_MEMORY_DB : str = Field("checkpoints.sqlite")

    DATABASE_URL : str = Field("postgresql+asyncpg://user:password@127.0.0.1:5432/diana")

    DEBUG:bool = Field(True)


settings = Settings()

logger = logging.getLogger(__name__)


