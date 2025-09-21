#!/usr/bin/env python3
"""
Simplified Coder-Buddy - Single shot generation
No complex loops, just direct generation
"""
import os
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from agent.states import Plan, File
from pydantic import BaseModel
from typing import List

load_dotenv()

class SimpleResponse(BaseModel):
    """Simple response format"""
    files: List[dict]  # List of {filename, content} dicts

def get_simple_llm():
    """Get simple, fast LLM"""
    return ChatOpenAI(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base=os.getenv("OPENAI_BASE_URL"),
        temperature=0.3,
        max_tokens=2048
    )

def simple_generate(prompt: str) -> bool:
    """Simple, direct generation"""
    print(f"🚀 Simple generation for: {prompt}")

    llm = get_simple_llm()

    # Single prompt that generates everything
    generation_prompt = f"""
Create a complete web project for: {prompt}

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
- Use inline styles if needed for simplicity
- Keep it clean and modern

Generate ONLY the JSON with the files array. No extra text.
"""

    try:
        print("⚡ Generating all files at once...")
        response = llm.invoke(generation_prompt)
        content = response.content.strip()

        # Try to parse as JSON
        import json
        try:
            data = json.loads(content)
            files_data = data.get("files", [])
        except:
            # Fallback: create a simple HTML file
            files_data = [{
                "filename": "index.html",
                "content": f'<!DOCTYPE html><html><head><title>Generated Project</title></head><body><h1 style="color: red;">Hello World</h1><p>Generated for: {prompt}</p></body></html>'
            }]

        # Create project directory
        project_dir = "generated_project"
        if os.path.exists(project_dir):
            import shutil
            shutil.rmtree(project_dir)

        os.makedirs(project_dir, exist_ok=True)

        # Write files
        for file_info in files_data:
            filename = file_info.get("filename", "index.html")
            content = file_info.get("content", "<!-- No content -->")

            file_path = os.path.join(project_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"📁 Created: {filename}")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Simple main function"""
    import sys

    print("🚀 SIMPLE CODER-BUDDY")
    print("=" * 30)

    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = input("Enter project description: ").strip()
        if not prompt:
            prompt = "Create a simple HTML page that says Hello World in red text"

    print(f"📝 Project: {prompt}")

    start_time = time.time()
    success = simple_generate(prompt)
    end_time = time.time()

    duration = end_time - start_time
    print(f"\n⏱️ Completed in {duration:.1f} seconds")

    if success:
        print("✅ Files generated in generated_project/")
        print("🌐 Open: open generated_project/index.html")

        # Show what was created
        if os.path.exists("generated_project"):
            files = os.listdir("generated_project")
            print(f"📁 Files: {', '.join(files)}")
    else:
        print("❌ Generation failed")

if __name__ == "__main__":
    main()