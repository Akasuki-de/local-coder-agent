#!/usr/bin/env python3
"""
Test script to verify IONOS AI Model Hub connection
"""
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_ionos_direct():
    """Test IONOS connection directly with requests first"""

    print("🔌 Testing IONOS AI Model Hub connection...")
    print(f"📡 Base URL: {os.getenv('OPENAI_BASE_URL')}")
    print(f"🤖 Model: {os.getenv('OPENAI_MODEL')}")
    print(f"🔑 API Key Length: {len(os.getenv('OPENAI_API_KEY', ''))}")

    try:
        # Test with direct requests first
        url = f"{os.getenv('OPENAI_BASE_URL')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": os.getenv('OPENAI_MODEL'),
            "messages": [
                {"role": "user", "content": "Say hello and confirm you're working through IONOS AI Model Hub!"}
            ],
            "temperature": 0.7,
            "max_tokens": 150
        }

        print("\n💬 Testing direct HTTP request...")
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"✅ Direct Response: {content}")
            return True
        else:
            print(f"❌ HTTP Error {response.status_code}: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Direct connection test failed: {e}")
        return False

def test_ionos_langchain():
    """Test IONOS connection with LangChain"""

    try:
        from langchain_openai import ChatOpenAI

        print("\n🦜 Testing LangChain integration...")

        # Initialize IONOS client using OpenAI-compatible interface
        llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "meta-llama/llama-3.1-8b-instruct"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_api_base=os.getenv("OPENAI_BASE_URL"),
            temperature=0.7,
        )

        # Test simple chat completion
        response = llm.invoke("Say hello from LangChain!")
        print(f"✅ LangChain Response: {response.content}")

        # Test structured output (like our agents will use)
        print("\n📋 Testing structured output capability...")
        from pydantic import BaseModel

        class TestSchema(BaseModel):
            greeting: str
            status: str
            confidence: float

        structured_llm = llm.with_structured_output(TestSchema)
        structured_response = structured_llm.invoke("Generate a greeting with status 'connected' and confidence level between 0.8-1.0")

        print(f"✅ Structured Response:")
        print(f"   • Greeting: {structured_response.greeting}")
        print(f"   • Status: {structured_response.status}")
        print(f"   • Confidence: {structured_response.confidence}")

        return True

    except Exception as e:
        print(f"❌ LangChain test failed: {e}")
        return False

if __name__ == "__main__":
    direct_success = test_ionos_direct()

    if direct_success:
        langchain_success = test_ionos_langchain()
        if langchain_success:
            print("\n🎉 All IONOS connection tests successful!")
        exit(0 if langchain_success else 1)
    else:
        print("\n❌ Direct connection failed, skipping LangChain test")
        exit(1)