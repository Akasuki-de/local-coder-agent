#!/usr/bin/env python3
"""
Debug script to check IONOS API access and available models
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def check_models():
    """Check what models are available"""
    print("🔍 Checking available models...")

    try:
        url = f"{os.getenv('OPENAI_BASE_URL')}/models"
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            models = response.json()
            print("✅ Available models:")
            for model in models.get('data', []):
                print(f"   • {model.get('id', 'Unknown')}")
            return models
        else:
            print(f"❌ Error: {response.text}")
            return None

    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def test_direct_api():
    """Test the direct API with minimal request"""
    print("\n🧪 Testing minimal API request...")

    # Try different model names that might be available
    test_models = [
        "meta-llama/llama-3.1-8b-instruct",
        "llama-3.1-8b-instruct",
        "meta-llama/llama-3.1-70b-instruct",
        "llama-3.1-70b-instruct"
    ]

    for model in test_models:
        print(f"\n🤖 Testing model: {model}")

        try:
            url = f"{os.getenv('OPENAI_BASE_URL')}/chat/completions"
            headers = {
                "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": model,
                "messages": [
                    {"role": "user", "content": "Hello"}
                ],
                "max_tokens": 10
            }

            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                print(f"✅ Success with {model}: {content}")
                return True
            else:
                print(f"❌ Failed {response.status_code}: {response.text}")

        except Exception as e:
            print(f"❌ Exception with {model}: {e}")

    return False

if __name__ == "__main__":
    print("🔧 IONOS API Debugging")
    print(f"Base URL: {os.getenv('OPENAI_BASE_URL')}")
    print(f"API Key (first 20 chars): {os.getenv('OPENAI_API_KEY', '')[:20]}...")

    models = check_models()
    success = test_direct_api()

    if not success:
        print("\n💡 Suggestions:")
        print("1. Check if your IONOS token is active")
        print("2. Verify you have access to AI Model Hub")
        print("3. Check if the model name format is correct")
        print("4. Try accessing the IONOS console to confirm your setup")