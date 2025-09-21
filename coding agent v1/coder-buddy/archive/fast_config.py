"""
Fast configuration for quick testing and development
Uses only the fastest models for all tasks
"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

def get_fast_llm() -> ChatOpenAI:
    """Get the fastest model for all tasks"""
    return ChatOpenAI(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base=os.getenv("OPENAI_BASE_URL"),
        temperature=0.3,
        max_tokens=4096,
        timeout=30  # 30 second timeout
    )

# Override the multi-model system for speed
def get_planner_llm_fast(complexity: str = "medium") -> ChatOpenAI:
    return get_fast_llm()

def get_architect_llm_fast(complexity: str = "medium") -> ChatOpenAI:
    return get_fast_llm()

def get_coder_llm_fast(complexity: str = "medium") -> ChatOpenAI:
    return get_fast_llm()