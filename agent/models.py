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
    temperature=0.1
)

gpt_oss_120b = ChatOpenAI(
    model="openai/gpt-oss-120b",
    api_key=OPENROUTER_API_KEY,
    base_url=BASE_URL,
    temperature=0.1,
    extra_body={
        "provider": {
            "order": ["groq"],
            "allow_fallbacks": True,
            "ignore": ["google-vertex"],
        }
    }
)

llama4_Scout = ChatOpenAI(
    model="meta-llama/llama-4-scout",
    api_key=OPENROUTER_API_KEY,
    base_url=BASE_URL,
    temperature=0.5,
    extra_body={
        "provider": {
            "sort": "latency",
            "allow_fallbacks": True,
            "ignore": ["google-vertex"]
        }
    }
)