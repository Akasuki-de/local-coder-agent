#!/usr/bin/env python3
"""
Test with the correct model name from IONOS
"""
import requests

def test_with_correct_model():
    """Test with the exact model name from IONOS"""
    new_token = "eyJ0eXAiOiJKV1QiLCJraWQiOiJmYzk2OWZmYS1jNDMzLTQ4NDctOGQwMS1lNTY3ZjUyNzkzMzMiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJpb25vc2Nsb3VkIiwiaWF0IjoxNzU2ODQ1MDkxLCJjbGllbnQiOiJVU0VSIiwiaWRlbnRpdHkiOnsiY29udHJhY3ROdW1iZXIiOjMzOTcxMDMzLCJyb2xlIjoib3duZXIiLCJyZWdEb21haW4iOiJpb25vcy5jb20iLCJyZXNlbGxlcklkIjoxLCJ1dWlkIjoiN2JjYjc4ODEtYWQzMS00MTA4LThiN2YtMDhiMjY3YmEyNGVlIiwicHJpdmlsZWdlcyI6WyJEQVRBX0NFTlRFUl9DUkVBVEUiLCJTTkFQU0hPVF9DUkVBVEUiLCJJUF9CTE9DS19SRVNFUlZFIiwiTUFOQUdFX0RBVEFQTEFURk9STSIsIkFDQ0VTU19BQ1RJVklUWV9MT0ciLCJQQ0NfQ1JFQVRFIiwiQUNDRVNTX1MzX09CSkVDVF9TVE9SQUdFIiwiQkFDS1VQX1VOSVRfQ1JFQVRFIiwiQ1JFQVRFX0lOVEVSTkVUX0FDQ0VTUyIsIks4U19DTFVTVEVSX0NSRUFURSIsIkZMT1dfTE9HX0NSRUFURSIsIkFDQ0VTU19BTkRfTUFOQUdFX01PTklUT1JJTkciLCJBQ0NFU1NfQU5EX01BTkFHRV9DRVJUSUZJQ0FURVMiLCJBQ0NFU1NfQU5EX01BTkFHRV9MT0dHSU5HIiwiTUFOQUdFX0RCQUFTIiwiQUNDRVNTX0FORF9NQU5BR0VfRE5TIiwiTUFOQUdFX1JFR0lTVFJZIiwiQUNDRVNTX0FORF9NQU5BR0VfQ0ROIiwiQUNDRVNTX0FORF9NQU5BR0VfVlBOIiwiQUNDRVNTX0FORF9NQU5BR0VfQVBJX0dBVEVXQVkiLCJBQ0NFU1NfQU5EX01BTkFHRV9OR1MiLCJBQ0NFU1NfQU5EX01BTkFHRV9LQUFTIiwiQUNDRVNTX0FORF9NQU5BR0VfTkVUV09SS19GSUxFX1NUT1JBR0UiLCJBQ0NFU1NfQU5EX01BTkFHRV9BSV9NT0RFTF9IVUIiLCJDUkVBVEVfTkVUV09SS19TRUNVUklUWV9HUk9VUFMiLCJBQ0NFU1NfQU5EX01BTkFHRV9JQU1fUkVTT1VSQ0VTIl0sImlzUGFyZW50IjpmYWxzZX0sImV4cCI6MTc4ODM4MTA5MX0.uigaOhWSnEd9zqDHWKfbWmEQ4HAgLorsC-7dA27Kjk33zmIrIBRsaBPjSmrXiY7JpQBPbgmjwuj717cPhUFR79Rt49CD_Hvi7ijlBW-JEb1_y-nLDGZ9B_wDgGyXGwYXBE-XJZVZEcyRow19yDW31uVnWkwmKa5KeRtlIMdr3Q6NDxPNaDC1CUBLIuEDvmklmG40ygH-4_dEq1Fn71fFuqyfBqVT5Ie9Sh0t3mLj4fMAfaffrNKNSqGps9u8mQCH_cpa8GjqLVBKeVZWWVBzy7BPFCkFd404biqrVlORxDt0b4UUKIGZHdzn3b9jPr0_B-UPLaqmwssXJlyuOXIt1w"

    print("🔧 Testing with Correct Model Names")
    print("=" * 50)

    # Test different model names from the available list
    models_to_test = [
        "meta-llama/Meta-Llama-3.1-8B-Instruct",  # Exact name from API
        "mistralai/Mistral-Nemo-Instruct-2407",
        "openGPT-X/Teuken-7B-instruct-commercial",
        "openai/gpt-oss-120b"
    ]

    headers = {
        "Authorization": f"Bearer {new_token}",
        "Content-Type": "application/json"
    }

    chat_url = "https://openai.inference.de-txl.ionos.com/v1/chat/completions"

    for model in models_to_test:
        print(f"\n🤖 Testing model: {model}")

        chat_payload = {
            "model": model,
            "messages": [{"role": "user", "content": "Say 'Hello from IONOS!' in exactly those words."}],
            "max_tokens": 20,
            "temperature": 0.1
        }

        try:
            response = requests.post(chat_url, json=chat_payload, headers=headers, timeout=20)
            print(f"   📊 Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                message = data['choices'][0]['message']['content']
                print(f"   ✅ SUCCESS: {message}")
                print(f"   🎯 Working model: {model}")
                return model
            else:
                error_text = response.text[:200]
                print(f"   ❌ Failed: {error_text}")

        except Exception as e:
            print(f"   💥 Exception: {e}")

    return None

if __name__ == "__main__":
    working_model = test_with_correct_model()
    if working_model:
        print(f"\n🎉 Found working model: {working_model}")
        print(f"✅ Ready to update configuration!")
    else:
        print(f"\n❌ No working models found")