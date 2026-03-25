from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"

nvidia_nemotron_3_super_120b_a12b = ChatOpenAI(
    model="nvidia/nemotron-3-super-120b-a12b",
    api_key=OPENROUTER_API_KEY,
    base_url=BASE_URL,
    temperature=0.5,
    model_kwargs={
        "reasoning": {
            "enabled": False
        }
    },
    extra_body={
        "provider": {
            "order": ["nebius/bf16"],
            "allow_fallbacks": False
        }
    }
)