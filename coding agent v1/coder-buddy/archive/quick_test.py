#!/usr/bin/env python3
"""
Quick test script using only fast models
"""
import os
import time
from fast_graph import fast_agent

def quick_test():
    """Run a quick test with the fast agent"""
    print("🚀 Running Quick Test with Fast Models Only")
    print("=" * 50)

    # Clean up previous run
    if os.path.exists("generated_project"):
        import shutil
        shutil.rmtree("generated_project")
        print("🧹 Cleaned previous project")

    start_time = time.time()

    try:
        print("📝 Testing: Simple HTML page with red text")
        print("⚡ Using: Llama-3.1-8B for ALL agents")
        print("🎯 Target: Under 2 minutes")
        print()

        result = fast_agent.invoke(
            {"user_prompt": "Create a simple HTML page that says Hello World in red text"},
            {"recursion_limit": 10}
        )

        end_time = time.time()
        duration = end_time - start_time

        print(f"\n🎉 Test completed in {duration:.1f} seconds!")

        # Check results
        if os.path.exists("generated_project"):
            files = os.listdir("generated_project")
            print(f"📁 Generated {len(files)} files: {files}")

            # Show content
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join("generated_project", file)
                    with open(file_path, 'r') as f:
                        content = f.read()
                        print(f"\n📄 {file} content:")
                        print(content[:200] + ("..." if len(content) > 200 else ""))

            print(f"\n🌐 Open result: open generated_project/index.html")
            return True
        else:
            print("❌ No files generated")
            return False

    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        print(f"❌ Test failed after {duration:.1f} seconds: {e}")
        return False

if __name__ == "__main__":
    success = quick_test()
    if success:
        print("\n✅ Fast configuration working!")
    else:
        print("\n❌ Fast configuration needs debugging")