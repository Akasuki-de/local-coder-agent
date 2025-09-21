#!/usr/bin/env python3
"""
🚀 CODER-BUDDY - Ultimate AI Development Platform
Lovable-style development with IONOS AI Model Hub

Features:
- Multi-model optimization for different task complexity
- Pre-built project templates for rapid development
- Intelligent complexity detection
- Interactive project creation
"""
import argparse
import sys
import os
from typing import Optional

from agent.graph import agent
from agent.multi_model_config import model_manager
from templates import PROJECT_TEMPLATES, list_templates, get_template
from enhanced_main import ProjectAnalyzer

def display_banner():
    """Display the main banner"""
    print("🚀 " + "="*70)
    print("   ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄  ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄")
    print("  █       █       █      ██       █       █")
    print("  █       █   ▄   █  ▄    █    ▄▄▄█   ▄▄▄▄█")
    print("  █     ▄▄█  █ █  █ █ █   █   █▄▄▄█  █▄▄▄▄▄")
    print("  █    █  █  █▄█  █ █▄█   █    ▄▄▄█▄▄▄▄▄  █")
    print("  █    █▄▄█       █       █   █▄▄▄ ▄▄▄▄▄█  █")
    print("  █▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄██▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█")
    print()
    print("           🤖 BUDDY - AI Development Platform")
    print("           Powered by IONOS AI Model Hub")
    print("="*70)

def display_main_menu():
    """Display the main interaction menu"""
    print("🎯 Choose your development approach:")
    print()
    print("1️⃣  🚀 QUICK START - Use pre-built templates")
    print("2️⃣  💬 CUSTOM PROJECT - Describe your own project")
    print("3️⃣  📚 EXAMPLES - See example prompts")
    print("4️⃣  🤖 MODELS - View available AI models")
    print("5️⃣  📖 HELP - Usage guide and tips")
    print("6️⃣  🚪 EXIT")
    print()

def handle_quick_start():
    """Handle template-based quick start"""
    print("🎨 " + "="*50)
    print("   QUICK START TEMPLATES")
    print("="*50)

    # Group templates by complexity
    simple_templates = {k: v for k, v in PROJECT_TEMPLATES.items()
                       if v['complexity'] == 'simple'}
    medium_templates = {k: v for k, v in PROJECT_TEMPLATES.items()
                       if v['complexity'] == 'medium'}
    complex_templates = {k: v for k, v in PROJECT_TEMPLATES.items()
                        if v['complexity'] == 'complex'}

    print("🟢 QUICK & SIMPLE (2-5 minutes):")
    for key, template in medium_templates.items():
        if 'landing' in key or 'simple' in template['name'].lower():
            print(f"   {key} - {template['name']}")

    print("\n🟡 MEDIUM COMPLEXITY (5-15 minutes):")
    for key, template in medium_templates.items():
        if 'landing' not in key:
            print(f"   {key} - {template['name']}")

    print("\n🔴 ADVANCED PROJECTS (15-30 minutes):")
    for key, template in complex_templates.items():
        print(f"   {key} - {template['name']}")

    print("\n💡 Type a template name (e.g., 'todo', 'portfolio') or 'back' to return:")

    while True:
        choice = input("➤ ").strip().lower()

        if choice == 'back':
            return None

        if choice in PROJECT_TEMPLATES:
            template = PROJECT_TEMPLATES[choice]
            print(f"\n✨ Selected: {template['name']}")
            print(f"📝 Description: {template['prompt'][:100]}...")
            print(f"⏱️  Estimated time: {template['estimated_time']}")

            confirm = input("\n🚀 Generate this project? (y/n): ").strip().lower()
            if confirm in ['y', 'yes']:
                return template['prompt']
            else:
                continue
        else:
            print("❌ Template not found. Available templates:")
            for key in PROJECT_TEMPLATES.keys():
                print(f"   • {key}")

def handle_custom_project():
    """Handle custom project creation"""
    print("💬 " + "="*50)
    print("   CUSTOM PROJECT CREATION")
    print("="*50)

    print("📝 Describe your project in detail. Include:")
    print("  • Main features and functionality")
    print("  • Design preferences (modern, minimal, etc.)")
    print("  • Technology requirements (if any)")
    print("  • Target devices (mobile, desktop, both)")
    print()
    print("💡 The more specific you are, the better the result!")
    print()

    while True:
        print("Enter your project description (or 'back' to return):")
        prompt = input("➤ ").strip()

        if prompt.lower() == 'back':
            return None

        if not prompt:
            print("❌ Please enter a project description")
            continue

        if len(prompt) < 10:
            print("❌ Please provide more details (at least 10 characters)")
            continue

        # Analyze complexity
        complexity, confidence = ProjectAnalyzer.analyze_complexity(prompt)
        print(f"\n🧠 Detected complexity: {complexity.upper()} (confidence: {confidence}%)")

        estimated_times = {
            "simple": "3-6 minutes",
            "medium": "6-15 minutes",
            "complex": "15-30 minutes"
        }
        print(f"⏱️  Estimated time: {estimated_times[complexity]}")

        confirm = input("\n🚀 Generate this project? (y/n): ").strip().lower()
        if confirm in ['y', 'yes']:
            return prompt

def display_examples():
    """Show example prompts"""
    print("📚 " + "="*50)
    print("   EXAMPLE PROMPTS")
    print("="*50)

    examples = {
        "🟢 Simple Projects": [
            "Create a landing page for a tech startup with hero section and contact form",
            "Build a simple calculator with basic arithmetic operations",
            "Make a personal business card website with contact info"
        ],
        "🟡 Medium Projects": [
            "Create a todo app with add/edit/delete and local storage persistence",
            "Build a weather app with current conditions and 5-day forecast",
            "Make a quiz app with multiple choice questions and score tracking"
        ],
        "🔴 Complex Projects": [
            "Create a blog platform with article management, search, and categories",
            "Build an e-commerce store with product catalog, cart, and checkout",
            "Make an admin dashboard with charts, tables, and user management"
        ]
    }

    for category, prompts in examples.items():
        print(f"\n{category}:")
        for prompt in prompts:
            print(f"   • {prompt}")

    input("\nPress Enter to continue...")

def display_help():
    """Display usage help"""
    print("📖 " + "="*50)
    print("   USAGE GUIDE")
    print("="*50)

    help_text = """
🎯 GETTING GREAT RESULTS:

1. BE SPECIFIC
   ✅ "Create a todo app with add/edit/delete, local storage, and dark mode"
   ❌ "Make an app"

2. MENTION DESIGN
   ✅ "Modern, clean design with blue and white colors"
   ❌ No design preferences

3. LIST FEATURES
   ✅ "Include user authentication, search, and responsive design"
   ❌ Vague functionality

4. SPECIFY PLATFORM
   ✅ "Mobile-first responsive design"
   ✅ "Desktop-only application"

🚀 MODEL OPTIMIZATION:
• Simple projects use fast models (2-5 min generation)
• Medium projects use balanced models (5-15 min)
• Complex projects use powerful models (15-30 min)

📁 OUTPUT:
• Files are generated in 'generated_project/' folder
• Open index.html in your browser to see the result
• All code is ready to use and modify

💡 TIPS:
• Use templates for faster generation
• Start simple, then iterate with improvements
• Check the generated README for project details
"""

    print(help_text)
    input("Press Enter to continue...")

def run_generation(prompt: str, recursion_limit: int = 100):
    """Run the actual project generation"""
    try:
        # Clean up previous generation
        if os.path.exists("generated_project"):
            import shutil
            shutil.rmtree("generated_project")
            print("🧹 Cleaned previous project")

        print(f"\n🚀 Starting generation...")
        print(f"📝 Project: {prompt}")

        # Analyze and show model selection
        complexity, confidence = ProjectAnalyzer.analyze_complexity(prompt)
        print(f"🧠 Complexity: {complexity.upper()} (confidence: {confidence}%)")

        print(f"\n⚡ Initializing {complexity} workflow...")
        print("🤖 This may take a few minutes...")
        print()

        # Run the agent
        result = agent.invoke(
            {"user_prompt": prompt},
            {"recursion_limit": recursion_limit}
        )

        print("\n🎉 " + "="*50)
        print("   GENERATION COMPLETED!")
        print("="*50)

        # Show results
        project_dir = "generated_project"
        if os.path.exists(project_dir):
            files = [f for f in os.listdir(project_dir) if os.path.isfile(os.path.join(project_dir, f))]
            print(f"📁 Generated {len(files)} files:")
            for file in files:
                print(f"   • {file}")

            print(f"\n🌐 To view your project:")
            print(f"   open {project_dir}/index.html")
            print(f"\n📂 Project location:")
            print(f"   {os.path.abspath(project_dir)}")
        else:
            print("❌ No files were generated. Check for errors above.")

    except KeyboardInterrupt:
        print("\n⏹️ Generation cancelled by user.")
    except Exception as e:
        print(f"\n❌ Generation failed: {e}")
        print("💡 Try simplifying your request or check your IONOS connection")

def main():
    """Main interactive application"""
    parser = argparse.ArgumentParser(description="Coder-Buddy AI Development Platform")
    parser.add_argument("--prompt", "-p", type=str, help="Skip interactive mode with direct prompt")
    parser.add_argument("--template", "-t", type=str, help="Use specific template")
    parser.add_argument("--recursion-limit", "-r", type=int, default=100, help="Recursion limit")
    parser.add_argument("--models", "-m", action="store_true", help="List available models")

    args = parser.parse_args()

    # Handle non-interactive modes
    if args.models:
        model_manager.list_available_models()
        return

    if args.template:
        template = get_template(args.template)
        if template:
            print(f"🎨 Using template: {template['name']}")
            run_generation(template['prompt'], args.recursion_limit)
        else:
            print(f"❌ Template '{args.template}' not found")
            list_templates()
        return

    if args.prompt:
        run_generation(args.prompt, args.recursion_limit)
        return

    # Interactive mode
    display_banner()

    while True:
        display_main_menu()
        choice = input("Choose an option (1-6): ").strip()

        if choice == '1':
            prompt = handle_quick_start()
            if prompt:
                run_generation(prompt, args.recursion_limit)

        elif choice == '2':
            prompt = handle_custom_project()
            if prompt:
                run_generation(prompt, args.recursion_limit)

        elif choice == '3':
            display_examples()

        elif choice == '4':
            model_manager.list_available_models()
            input("Press Enter to continue...")

        elif choice == '5':
            display_help()

        elif choice == '6':
            print("👋 Thanks for using Coder-Buddy!")
            sys.exit(0)

        else:
            print("❌ Invalid choice. Please select 1-6.")

if __name__ == "__main__":
    main()