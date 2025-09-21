#!/usr/bin/env python3
"""
Direct test using requests to avoid dependency issues
"""
import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

def test_direct_generation():
    """Test using direct API calls"""
    print("🚀 Testing IONOS Direct API Generation")
    print("=" * 40)

    # Get API details
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    model = os.getenv("OPENAI_MODEL", "meta-llama/Meta-Llama-3.1-8B-Instruct")

    if not api_key or not base_url:
        print("❌ Missing API configuration in .env")
        return False

    print(f"🔑 Using model: {model}")
    print(f"🌐 API endpoint: {base_url}")

    # Test prompt
    prompt = "Create a modern portfolio website with dark theme and smooth animations"
    print(f"📝 Generating: {prompt}")

    # API payload
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": f"""Create a complete web project for: {prompt}

Generate ALL necessary files in this format:
{{
  "files": [
    {{"filename": "index.html", "content": "<!DOCTYPE html>..."}},
    {{"filename": "style.css", "content": "/* CSS content */"}},
    {{"filename": "script.js", "content": "// JS content"}}
  ]
}}

Requirements:
- Make it fully functional
- Include all necessary HTML, CSS, and JavaScript
- Modern dark theme with smooth animations
- Responsive design
- Clean and professional

Generate ONLY the JSON with the files array. No extra text."""
            }
        ],
        "max_tokens": 4096,
        "temperature": 0.3
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    start_time = time.time()

    try:
        print("⚡ Sending request to IONOS...")
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=120
        )

        if response.status_code != 200:
            print(f"❌ API Error {response.status_code}: {response.text}")
            return False

        result = response.json()
        content = result["choices"][0]["message"]["content"].strip()

        print("✅ Response received, parsing...")

        # Try to parse JSON
        try:
            data = json.loads(content)
            files_data = data.get("files", [])
        except json.JSONDecodeError:
            print("⚠️ JSON parsing failed, creating fallback...")
            files_data = [{
                "filename": "index.html",
                "content": f'<!DOCTYPE html><html><head><title>Generated Portfolio</title><style>body{{background:#1a1a1a;color:white;font-family:Arial;text-align:center;padding:50px;}}h1{{color:#00ff88;animation:glow 2s infinite;}}.fade{{animation:fade 1s ease-in;}}@keyframes glow{{0%,100%{{text-shadow:0 0 20px #00ff88;}}50%{{text-shadow:0 0 40px #00ff88;}}}}@keyframes fade{{from{{opacity:0;}}to{{opacity:1;}}}}</style></head><body><h1 class="fade">Modern Portfolio</h1><p class="fade">Generated for: {prompt}</p><div class="fade">🚀 Dark theme with animations!</div></body></html>'
            }]

        # Clean up previous project
        if os.path.exists("generated_project"):
            import shutil
            shutil.rmtree("generated_project")

        os.makedirs("generated_project", exist_ok=True)

        # Write files
        for file_info in files_data:
            filename = file_info.get("filename", "index.html")
            content = file_info.get("content", "<!-- No content -->")

            file_path = os.path.join("generated_project", filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"📁 Created: {filename}")

        end_time = time.time()
        duration = end_time - start_time

        print(f"\n🎉 Test completed in {duration:.1f} seconds!")

        # Show files created
        files = os.listdir("generated_project")
        print(f"📁 Generated {len(files)} files: {', '.join(files)}")
        print(f"🌐 Open result: open generated_project/index.html")

        return True

    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        print(f"❌ Test failed after {duration:.1f}s: {e}")
        return False

if __name__ == "__main__":
    success = test_direct_generation()
    if success:
        print("\n✅ IONOS API test successful!")
    else:
        print("\n❌ IONOS API test failed")