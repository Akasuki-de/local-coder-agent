"""
Configuration module for AI model providers
Supports IONOS, Groq, and OpenAI with automatic fallback
"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

load_dotenv()

def get_llm():
    """
    Get the configured LLM client with automatic provider detection
    Priority: IONOS > Groq > OpenAI
    """

    # Option 1: IONOS AI Model Hub (preferred)
    if os.getenv("OPENAI_API_KEY") and os.getenv("OPENAI_BASE_URL"):
        print("🚀 Using IONOS AI Model Hub")
        return ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "meta-llama/llama-3.1-8b-instruct"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_api_base=os.getenv("OPENAI_BASE_URL"),
            temperature=0.7,
        )

    # Option 2: Groq (fallback)
    elif os.getenv("GROQ_API_KEY"):
        print("🔄 Falling back to Groq")
        return ChatGroq(
            model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
            groq_api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.7,
        )

    # Option 3: OpenAI (if configured)
    elif os.getenv("OPENAI_API_KEY") and not os.getenv("OPENAI_BASE_URL"):
        print("🤖 Using OpenAI")
        return ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.7,
        )

    else:
        raise ValueError(
            "No AI provider configured! Please set up one of:\n"
            "1. IONOS: OPENAI_API_KEY + OPENAI_BASE_URL\n"
            "2. Groq: GROQ_API_KEY\n"
            "3. OpenAI: OPENAI_API_KEY (without BASE_URL)"
        )

def test_llm_connection():
    """Test the configured LLM connection"""
    try:
        llm = get_llm()
        response = llm.invoke("Say 'Hello from AI agent!' in exactly those words.")
        print(f"✅ Connection successful: {response.content}")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False