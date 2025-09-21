#!/usr/bin/env python3
"""
Local Coder-Buddy using DeepSeek via Ollama
Lovable-like experience with local models
"""
import os
import json
import time
import subprocess
import shutil
from typing import Optional

def test_deepseek_available():
    """Test if DeepSeek is available via Ollama"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=10)
        return 'deepseek-coder' in result.stdout
    except:
        return False

def generate_with_deepseek(prompt: str) -> Optional[dict]:
    """Generate project using local DeepSeek model"""

    generation_prompt = f"""Create a complete web project for: {prompt}

Generate ALL necessary files in this exact JSON format:
{{
  "files": [
    {{"filename": "index.html", "content": "<!DOCTYPE html>..."}},
    {{"filename": "style.css", "content": "/* CSS content */"}},
    {{"filename": "script.js", "content": "// JS content"}}
  ]
}}

Requirements:
- Make it fully functional with modern design
- Include all necessary HTML, CSS, and JavaScript
- Use responsive design principles
- Add smooth animations and transitions
- Ensure clean, production-ready code
- Handle edge cases and errors

Generate ONLY the JSON with the files array. No extra text or explanation."""

    try:
        # Use ollama run with the prompt
        result = subprocess.run([
            'ollama', 'run', 'deepseek-coder:latest'
        ], input=generation_prompt, capture_output=True, text=True, timeout=300)

        if result.returncode != 0:
            print(f"❌ Ollama error: {result.stderr}")
            return None

        response = result.stdout.strip()

        # Try to parse JSON from response
        try:
            # Look for JSON in the response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1

            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
            else:
                print("⚠️ No valid JSON found in response")
                return create_fallback_project(prompt)

        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parsing failed: {e}")
            return create_fallback_project(prompt)

    except subprocess.TimeoutExpired:
        print("⏰ DeepSeek generation timed out")
        return None
    except Exception as e:
        print(f"❌ Error with DeepSeek: {e}")
        return None

def create_fallback_project(prompt: str) -> dict:
    """Create a basic fallback project if parsing fails"""
    return {
        "files": [
            {
                "filename": "index.html",
                "content": f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated Project</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }}
        .container {{
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            backdrop-filter: blur(10px);
        }}
        h1 {{
            animation: glow 2s infinite alternate;
        }}
        @keyframes glow {{
            from {{ text-shadow: 0 0 20px #fff; }}
            to {{ text-shadow: 0 0 30px #fff, 0 0 40px #667eea; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Project Generated!</h1>
        <p><strong>Request:</strong> {prompt}</p>
        <p>Generated with local DeepSeek model via Ollama</p>
    </div>
</body>
</html>'''
            }
        ]
    }

def local_generate(prompt: str) -> bool:
    """Generate project using local DeepSeek"""
    print(f"🏠 LOCAL CODER-BUDDY (DeepSeek)")
    print(f"🧠 Using: deepseek-coder:latest")
    print(f"📝 Generating: {prompt}")
    print("=" * 50)

    # Check DeepSeek availability
    if not test_deepseek_available():
        print("❌ DeepSeek not available. Run: ollama pull deepseek-coder")
        return False

    start_time = time.time()

    # Clean previous project
    if os.path.exists("generated_project"):
        shutil.rmtree("generated_project")
        print("🧹 Cleaned previous project")

    print("⚡ Generating with DeepSeek...")

    # Generate with DeepSeek
    files_data = generate_with_deepseek(prompt)

    if not files_data:
        print("❌ Generation failed")
        return False

    # Create project directory
    os.makedirs("generated_project", exist_ok=True)

    # Write files
    files_list = files_data.get("files", [])
    for file_info in files_list:
        filename = file_info.get("filename", "index.html")
        content = file_info.get("content", "<!-- No content -->")

        file_path = os.path.join("generated_project", filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"📁 Created: {filename}")

    end_time = time.time()
    duration = end_time - start_time

    print(f"\n🎉 Local generation completed in {duration:.1f} seconds!")
    print(f"📁 Generated {len(files_list)} files")
    print(f"🌐 Open: open generated_project/index.html")

    # Show preview of main file
    main_file = "generated_project/index.html"
    if os.path.exists(main_file):
        with open(main_file, 'r') as f:
            content = f.read()
            print(f"\n📄 Preview:")
            print(content[:200] + ("..." if len(content) > 200 else ""))

    return True

def main():
    """Main function for local coder-buddy"""
    import sys

    print("🏠 LOCAL CODER-BUDDY")
    print("Powered by DeepSeek + Ollama")
    print("=" * 40)

    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        print("📝 Enter your project description:")
        prompt = input("➤ ").strip()
        if not prompt:
            prompt = "Create a simple HTML page that says Hello World with modern styling"

    success = local_generate(prompt)

    if success:
        print("\n✅ Local generation successful!")
        print("💡 Tip: Try more complex projects - no rate limits!")
    else:
        print("\n❌ Local generation failed")
        print("💡 Try: ollama pull deepseek-coder")

if __name__ == "__main__":
    main()