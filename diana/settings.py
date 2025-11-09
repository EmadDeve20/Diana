import os
import logging

from dotenv import load_dotenv


load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

PROXY_URL = os.getenv("PROXY_URL") or None


logger = logging.getLogger(__name__)


