from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logger = logging.getLogger(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"

logger.info(f"Initializing model qwen/qwen3.5-flash-02-23 with base_url={BASE_URL}")

qwen35_flash = ChatOpenAI(
    model="qwen/qwen3.5-flash-02-23",
    api_key=OPENROUTER_API_KEY,
    base_url=BASE_URL,
    temperature=0.5
)