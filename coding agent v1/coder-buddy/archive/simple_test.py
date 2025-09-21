#!/usr/bin/env python3
"""
Simple test with basic HTML - should complete quickly
"""
from agent.graph import agent
import os

def test_simple_html():
    """Test with a very simple HTML request"""
    print("🌐 Testing Simple HTML Generation")
    print("=" * 50)

    # Very simple prompt
    simple_prompt = "Create a single HTML file that says 'Hello IONOS!' in red text"

    try:
        print(f"📝 Prompt: {simple_prompt}")
        print("🚀 Running agent with simple request...")

        # Run with lower recursion limit for faster completion
        result = agent.invoke(
            {"user_prompt": simple_prompt},
            {"recursion_limit": 20}
        )

        print("✅ Agent completed!")
        print(f"📊 Result keys: {list(result.keys())}")

        # Check generated files
        project_dir = "generated_project"
        if os.path.exists(project_dir):
            files = os.listdir(project_dir)
            print(f"📁 Generated files: {files}")

            # Show content of generated files
            for file in files:
                file_path = os.path.join(project_dir, file)
                if os.path.isfile(file_path):
                    print(f"\n📄 Content of {file}:")
                    with open(file_path, 'r') as f:
                        content = f.read()
                        print(content[:300] + ("..." if len(content) > 300 else ""))
        else:
            print("📁 No generated_project directory found")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Clean up any previous runs
    if os.path.exists("generated_project"):
        import shutil
        shutil.rmtree("generated_project")
        print("🧹 Cleaned up previous generated_project")

    success = test_simple_html()
    if success:
        print("\n🎉 Simple HTML test successful!")
        print("💡 Ready for more complex projects!")
    else:
        print("\n❌ Test failed - let's debug")