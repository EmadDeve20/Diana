# TODO: Change Settings and use pydantic_settings to keep settings parameters

import os
import logging

from dotenv import load_dotenv


load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

PROXY_URL = os.getenv("PROXY_URL") or None

HUGGINGFACE_KEY = os.getenv("HUGGINGFACE_KEY")

MODEL = os.getenv("MODEL")

TEMPERATURE = float(os.getenv("TEMPERATURE") or "0")

SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")

OWNER_USERNAME = os.getenv("OWNER_USERNAME")

AI_MEMORY_DB = os.getenv("AI_MEMORY_DB") or "checkpoints.sqlite"

DATABASE_URL = os.getenv("DATABASE_URL") or "postgresql+asyncpg://user:password@127.0.0.1:5432/diana"

DEBUG:str = os.getenv("DEBUG") or "true"

DEBUG:bool = True if DEBUG.lower() == "true" else False

logger = logging.getLogger(__name__)


