#!/usr/bin/env python3
"""
Test the provided IONOS token directly
"""
import requests
import json

def test_ionos_token():
    """Test the new IONOS token"""
    # Your new token
    new_token = "eyJ0eXAiOiJKV1QiLCJraWQiOiJmYzk2OWZmYS1jNDMzLTQ4NDctOGQwMS1lNTY3ZjUyNzkzMzMiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJpb25vc2Nsb3VkIiwiaWF0IjoxNzU2ODQ1MDkxLCJjbGllbnQiOiJVU0VSIiwiaWRlbnRpdHkiOnsiY29udHJhY3ROdW1iZXIiOjMzOTcxMDMzLCJyb2xlIjoib3duZXIiLCJyZWdEb21haW4iOiJpb25vcy5jb20iLCJyZXNlbGxlcklkIjoxLCJ1dWlkIjoiN2JjYjc4ODEtYWQzMS00MTA4LThiN2YtMDhiMjY3YmEyNGVlIiwicHJpdmlsZWdlcyI6WyJEQVRBX0NFTlRFUl9DUkVBVEUiLCJTTkFQU0hPVF9DUkVBVEUiLCJJUF9CTE9DS19SRVNFUlZFIiwiTUFOQUdFX0RBVEFQTEFURk9STSIsIkFDQ0VTU19BQ1RJVklUWV9MT0ciLCJQQ0NfQ1JFQVRFIiwiQUNDRVNTX1MzX09CSkVDVF9TVE9SQUdFIiwiQkFDS1VQX1VOSVRfQ1JFQVRFIiwiQ1JFQVRFX0lOVEVSTkVUX0FDQ0VTUyIsIks4U19DTFVTVEVSX0NSRUFURSIsIkZMT1dfTE9HX0NSRUFURSIsIkFDQ0VTU19BTkRfTUFOQUdFX01PTklUT1JJTkciLCJBQ0NFU1NfQU5EX01BTkFHRV9DRVJUSUZJQ0FURVMiLCJBQ0NFU1NfQU5EX01BTkFHRV9MT0dHSU5HIiwiTUFOQUdFX0RCQUFTIiwiQUNDRVNTX0FORF9NQU5BR0VfRE5TIiwiTUFOQUdFX1JFR0lTVFJZIiwiQUNDRVNTX0FORF9NQU5BR0VfQ0ROIiwiQUNDRVNTX0FORF9NQU5BR0VfVlBOIiwiQUNDRVNTX0FORF9NQU5BR0VfQVBJX0dBVEVXQVkiLCJBQ0NFU1NfQU5EX01BTkFHRV9OR1MiLCJBQ0NFU1NfQU5EX01BTkFHRV9LQUFTIiwiQUNDRVNTX0FORF9NQU5BR0VfTkVUV09SS19GSUxFX1NUT1JBR0UiLCJBQ0NFU1NfQU5EX01BTkFHRV9BSV9NT0RFTF9IVUIiLCJDUkVBVEVfTkVUV09SS19TRUNVUklUWV9HUk9VUFMiLCJBQ0NFU1NfQU5EX01BTkFHRV9JQU1fUkVTT1VSQ0VTIl0sImlzUGFyZW50IjpmYWxzZX0sImV4cCI6MTc4ODM4MTA5MX0.uigaOhWSnEd9zqDHWKfbWmEQ4HAgLorsC-7dA27Kjk33zmIrIBRsaBPjSmrXiY7JpQBPbgmjwuj717cPhUFR79Rt49CD_Hvi7ijlBW-JEb1_y-nLDGZ9B_wDgGyXGwYXBE-XJZVZEcyRow19yDW31uVnWkwmKa5KeRtlIMdr3Q6NDxPNaDC1CUBLIuEDvmklmG40ygH-4_dEq1Fn71fFuqyfBqVT5Ie9Sh0t3mLj4fMAfaffrNKNSqGps9u8mQCH_cpa8GjqLVBKeVZWWVBzy7BPFCkFd404biqrVlORxDt0b4UUKIGZHdzn3b9jPr0_B-UPLaqmwssXJlyuOXIt1w"

    print("🔑 Testing New IONOS Token")
    print("=" * 50)
    print(f"🧪 Token length: {len(new_token)}")

    # Test models endpoint first
    url = "https://openai.inference.de-txl.ionos.com/v1/models"
    headers = {
        "Authorization": f"Bearer {new_token}",
        "Content-Type": "application/json"
    }

    try:
        print("📋 Testing /models endpoint...")
        response = requests.get(url, headers=headers, timeout=10)

        print(f"📊 Status Code: {response.status_code}")

        if response.status_code == 200:
            print("✅ SUCCESS! Models endpoint working")
            data = response.json()
            models = [m.get('id', 'unknown') for m in data.get('data', [])]
            print(f"🤖 Found {len(models)} available models:")
            for i, model in enumerate(models[:10]):  # Show first 10
                print(f"   {i+1}. {model}")
            if len(models) > 10:
                print(f"   ... and {len(models) - 10} more models")

            # Test chat completion
            print("\n💬 Testing chat completion...")
            chat_url = "https://openai.inference.de-txl.ionos.com/v1/chat/completions"
            chat_payload = {
                "model": "meta-llama/llama-3.1-8b-instruct",
                "messages": [{"role": "user", "content": "Say 'Hello from IONOS AI Model Hub!' and nothing else."}],
                "max_tokens": 50,
                "temperature": 0.1
            }

            chat_response = requests.post(chat_url, json=chat_payload, headers=headers, timeout=20)
            print(f"📊 Chat Status: {chat_response.status_code}")

            if chat_response.status_code == 200:
                chat_data = chat_response.json()
                message = chat_data['choices'][0]['message']['content']
                print(f"✅ Chat Response: {message}")
                print("\n🎉 IONOS connection fully working!")
                return True
            else:
                print(f"❌ Chat failed: {chat_response.text}")
                return False

        else:
            print(f"❌ Models endpoint failed: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    success = test_ionos_token()
    if success:
        print("\n✅ Ready to update .env file!")
    else:
        print("\n❌ Token test failed")