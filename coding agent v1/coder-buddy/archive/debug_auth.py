#!/usr/bin/env python3
"""
IONOS Authentication Debugging Script
This will help identify the exact cause of the 401 error
"""
import os
import json
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

def decode_jwt_header(token):
    """Decode JWT header to check token format"""
    try:
        # JWT tokens have 3 parts separated by dots
        parts = token.split('.')
        if len(parts) != 3:
            return None, "Invalid JWT format - should have 3 parts separated by dots"

        # Decode header (first part)
        header_b64 = parts[0]
        # Add padding if needed
        header_b64 += '=' * (4 - len(header_b64) % 4)
        header_bytes = base64.urlsafe_b64decode(header_b64)
        header = json.loads(header_bytes)

        # Decode payload (second part)
        payload_b64 = parts[1]
        payload_b64 += '=' * (4 - len(payload_b64) % 4)
        payload_bytes = base64.urlsafe_b64decode(payload_b64)
        payload = json.loads(payload_bytes)

        return {"header": header, "payload": payload}, None
    except Exception as e:
        return None, f"JWT decode error: {e}"

def test_auth_variations():
    """Test different authentication approaches"""

    token = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")

    print("🔍 IONOS Authentication Debug")
    print(f"📍 Base URL: {base_url}")
    print(f"🔑 Token length: {len(token) if token else 0}")

    # Decode JWT to check its contents
    jwt_data, error = decode_jwt_header(token)
    if jwt_data:
        print(f"✅ JWT Format Valid")
        print(f"   • Algorithm: {jwt_data['header'].get('alg', 'unknown')}")
        print(f"   • Type: {jwt_data['header'].get('typ', 'unknown')}")
        print(f"   • Issuer: {jwt_data['payload'].get('iss', 'unknown')}")

        # Check expiration
        exp = jwt_data['payload'].get('exp')
        if exp:
            import datetime
            exp_date = datetime.datetime.fromtimestamp(exp)
            now = datetime.datetime.now()
            print(f"   • Expires: {exp_date}")
            print(f"   • Is Expired: {'Yes' if exp_date < now else 'No'}")

        # Check privileges
        privileges = jwt_data['payload'].get('identity', {}).get('privileges', [])
        ai_hub_access = 'ACCESS_AND_MANAGE_AI_MODEL_HUB' in privileges
        print(f"   • AI Model Hub Access: {'Yes' if ai_hub_access else 'No'}")

    else:
        print(f"❌ JWT Error: {error}")

    # Test different auth header formats
    auth_formats = [
        ("Bearer", f"Bearer {token}"),
        ("Authorization", f"Authorization: Bearer {token}"),
        ("X-API-Key", token),
        ("Authorization-Plain", token)
    ]

    # Test different endpoints
    endpoints = [
        "/models",
        "/chat/completions"
    ]

    for endpoint in endpoints:
        print(f"\n🧪 Testing endpoint: {endpoint}")
        url = f"{base_url}{endpoint}"

        for auth_name, auth_value in auth_formats:
            print(f"   🔐 Trying {auth_name} format...")

            if auth_name == "Bearer":
                headers = {"Authorization": auth_value, "Content-Type": "application/json"}
            elif auth_name == "X-API-Key":
                headers = {"X-API-Key": auth_value, "Content-Type": "application/json"}
            elif auth_name == "Authorization-Plain":
                headers = {"Authorization": auth_value, "Content-Type": "application/json"}
            else:
                headers = {"Content-Type": "application/json"}
                headers[auth_name] = auth_value

            try:
                if endpoint == "/models":
                    response = requests.get(url, headers=headers, timeout=10)
                else:
                    # Minimal chat request
                    payload = {
                        "model": "meta-llama/llama-3.1-8b-instruct",
                        "messages": [{"role": "user", "content": "hi"}],
                        "max_tokens": 5
                    }
                    response = requests.post(url, json=payload, headers=headers, timeout=10)

                print(f"      📊 Status: {response.status_code}")

                if response.status_code == 200:
                    print(f"      ✅ SUCCESS!")
                    if endpoint == "/models":
                        data = response.json()
                        models = [m.get('id', 'unknown') for m in data.get('data', [])]
                        print(f"      🤖 Available models: {models[:3]}{'...' if len(models) > 3 else ''}")
                    return True
                elif response.status_code == 401:
                    error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
                    print(f"      ❌ Auth failed: {error_data}")
                else:
                    print(f"      ⚠️  Other error: {response.text[:100]}")

            except requests.exceptions.Timeout:
                print(f"      ⏰ Timeout")
            except Exception as e:
                print(f"      💥 Exception: {e}")

    return False

def test_ionos_specific_auth():
    """Test IONOS-specific authentication patterns"""
    print("\n🏢 Testing IONOS-specific patterns...")

    token = os.getenv("OPENAI_API_KEY")

    # Test direct IONOS API (not OpenAI-compatible)
    ionos_endpoints = [
        "https://api.ionos.com/inference-openai/v1/models",
        "https://api.ionos.com/inference/v1/models",
        "https://openai.inference.de-txl.ionos.com/v1/models"
    ]

    for endpoint in ionos_endpoints:
        print(f"🔗 Testing: {endpoint}")

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(endpoint, headers=headers, timeout=10)
            print(f"   📊 Status: {response.status_code}")

            if response.status_code == 200:
                print(f"   ✅ SUCCESS with {endpoint}")
                data = response.json()
                print(f"   📄 Response: {json.dumps(data, indent=2)[:200]}...")
                return endpoint
            else:
                print(f"   ❌ Failed: {response.text[:100]}")

        except Exception as e:
            print(f"   💥 Exception: {e}")

    return None

if __name__ == "__main__":
    print("=" * 60)
    success = test_auth_variations()

    if not success:
        working_endpoint = test_ionos_specific_auth()

        if working_endpoint:
            print(f"\n✅ Found working endpoint: {working_endpoint}")
        else:
            print(f"\n❌ All authentication attempts failed")
            print(f"\n💡 Next steps:")
            print(f"   1. Generate a fresh token in IONOS console")
            print(f"   2. Verify AI Model Hub is enabled in your account")
            print(f"   3. Check if you're using the correct regional endpoint")
            print(f"   4. Contact IONOS support if issue persists")

    print("=" * 60)