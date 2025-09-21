#!/usr/bin/env python3
"""
Quick test for new IONOS token
Run this before updating your .env file
"""
import requests
import json

def test_new_token():
    """Test a new IONOS token"""
    print("🔑 IONOS Token Tester")
    print("=" * 50)

    # Get new token from user
    new_token = input("Paste your new IONOS token here: ").strip()

    if not new_token:
        print("❌ No token provided")
        return False

    print(f"🧪 Testing token (length: {len(new_token)})")

    # Test the token
    url = "https://openai.inference.de-txl.ionos.com/v1/models"
    headers = {
        "Authorization": f"Bearer {new_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            print("✅ SUCCESS! Token is working")
            data = response.json()
            models = [m.get('id', 'unknown') for m in data.get('data', [])]
            print(f"🤖 Available models: {len(models)} total")
            for model in models[:5]:  # Show first 5 models
                print(f"   • {model}")
            if len(models) > 5:
                print(f"   • ... and {len(models) - 5} more")

            # Test chat completion
            print("\n💬 Testing chat completion...")
            chat_url = "https://openai.inference.de-txl.ionos.com/v1/chat/completions"
            chat_payload = {
                "model": "meta-llama/llama-3.1-8b-instruct",
                "messages": [{"role": "user", "content": "Say 'Hello from IONOS!'"}],
                "max_tokens": 20
            }

            chat_response = requests.post(chat_url, json=chat_payload, headers=headers, timeout=15)

            if chat_response.status_code == 200:
                chat_data = chat_response.json()
                message = chat_data['choices'][0]['message']['content']
                print(f"✅ Chat test successful: {message}")

                print("\n🎉 Ready to update your .env file!")
                print(f"Add this line to your .env:")
                print(f"OPENAI_API_KEY={new_token}")
                return True
            else:
                print(f"❌ Chat test failed: {chat_response.text}")
                return False

        else:
            print(f"❌ Token test failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    test_new_token()