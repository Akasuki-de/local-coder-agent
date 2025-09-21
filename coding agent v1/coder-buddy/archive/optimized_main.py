#!/usr/bin/env python3
"""
Optimized Coder-Buddy with Performance Fixes
- Uses faster model selection
- Reduced complexity detection
- Better timeout handling
"""
import argparse
import sys
import os
import time
from typing import Optional

# Import the fast agent for better performance
from fast_graph import fast_agent

def simple_complexity_detection(prompt: str) -> str:
    """Simple and fast complexity detection"""
    prompt_lower = prompt.lower()

    # Very fast keyword detection
    complex_keywords = ['dashboard', 'admin', 'e-commerce', 'authentication', 'database', 'api']
    simple_keywords = ['simple', 'basic', 'hello', 'single page', 'minimal']

    if any(keyword in prompt_lower for keyword in complex_keywords):
        return "complex"
    elif any(keyword in prompt_lower for keyword in simple_keywords):
        return "simple"
    else:
        return "medium"

def display_banner():
    """Quick banner"""
    print("🚀 CODER-BUDDY (Optimized)")
    print("Fast AI Development Platform")
    print("=" * 40)

def main():
    """Optimized main function"""
    parser = argparse.ArgumentParser(description="Optimized Coder-Buddy")
    parser.add_argument("--prompt", "-p", type=str, help="Project prompt")
    parser.add_argument("--template", "-t", type=str, help="Use template")
    parser.add_argument("--timeout", type=int, default=120, help="Timeout in seconds")

    args = parser.parse_args()

    display_banner()

    # Get prompt
    if args.prompt:
        prompt = args.prompt
    elif args.template:
        # Simple templates
        templates = {
            "hello": "Create a simple HTML page that says Hello World in red text",
            "todo": "Create a basic todo list with add and delete functionality",
            "calc": "Create a simple calculator with basic operations"
        }
        prompt = templates.get(args.template, templates["hello"])
    else:
        print("📝 Enter your project description:")
        prompt = input("➤ ").strip()
        if not prompt:
            prompt = "Create a simple HTML page that says Hello World in red text"

    # Quick complexity detection
    complexity = simple_complexity_detection(prompt)
    print(f"🧠 Complexity: {complexity.upper()}")
    print(f"⚡ Using fast models for all agents")

    estimated_time = {"simple": "30-60s", "medium": "1-2min", "complex": "2-3min"}
    print(f"⏱️ Estimated time: {estimated_time[complexity]}")

    # Clean previous project
    if os.path.exists("generated_project"):
        import shutil
        shutil.rmtree("generated_project")
        print("🧹 Cleaned previous project")

    print(f"\n🚀 Generating: {prompt}")
    start_time = time.time()

    try:
        # Use fast agent with timeout
        result = fast_agent.invoke(
            {"user_prompt": prompt},
            {"recursion_limit": 8}  # Lower limit for speed
        )

        end_time = time.time()
        duration = end_time - start_time

        print(f"\n🎉 Completed in {duration:.1f} seconds!")

        # Check results
        if os.path.exists("generated_project"):
            files = [f for f in os.listdir("generated_project")
                    if os.path.isfile(os.path.join("generated_project", f))]
            print(f"📁 Generated {len(files)} files: {', '.join(files)}")
            print(f"🌐 Open: open generated_project/index.html")

            # Show a snippet of the main file
            main_file = "generated_project/index.html"
            if os.path.exists(main_file):
                with open(main_file, 'r') as f:
                    content = f.read()
                    print(f"\n📄 Preview:")
                    print(content[:150] + ("..." if len(content) > 150 else ""))

        else:
            print("❌ No files generated")
            return False

        return True

    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        print(f"❌ Failed after {duration:.1f}s: {str(e)[:100]}...")

        # Check if partial files were created
        if os.path.exists("generated_project"):
            files = os.listdir("generated_project")
            if files:
                print(f"⚠️ Partial generation: {files}")
                print("🌐 You can still check: open generated_project/index.html")

        return False

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n✅ Generation successful!")
        else:
            print("\n❌ Generation incomplete")
    except KeyboardInterrupt:
        print("\n⏹️ Cancelled by user")
        sys.exit(0)