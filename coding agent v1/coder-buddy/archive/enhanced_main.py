#!/usr/bin/env python3
"""
Enhanced Coder-Buddy with Multi-Model Optimization
Lovable-style AI development platform powered by IONOS AI Model Hub
"""
import argparse
import sys
import re
from typing import Tuple

from agent.graph import agent
from agent.multi_model_config import model_manager

class ProjectAnalyzer:
    """Analyzes project prompts to determine complexity and optimize model selection"""

    COMPLEXITY_INDICATORS = {
        "simple": [
            "single page", "basic", "simple", "minimal", "quick", "landing page",
            "hello world", "display", "show", "static"
        ],
        "complex": [
            "dashboard", "admin panel", "e-commerce", "blog platform", "cms",
            "authentication", "database", "api", "real-time", "chat app",
            "multi-page", "responsive", "animation", "interactive", "game"
        ]
    }

    FEATURE_WEIGHTS = {
        "crud": 2, "database": 2, "authentication": 3, "real-time": 3,
        "responsive": 1, "animation": 1, "api": 2, "charts": 2,
        "form": 1, "validation": 1, "search": 1, "filter": 1
    }

    @classmethod
    def analyze_complexity(cls, prompt: str) -> Tuple[str, int]:
        """
        Analyze prompt complexity based on keywords and features

        Returns:
            Tuple of (complexity_level, confidence_score)
        """
        prompt_lower = prompt.lower()
        complexity_score = 0
        feature_count = 0

        # Check for complexity indicators
        simple_count = sum(1 for keyword in cls.COMPLEXITY_INDICATORS["simple"]
                          if keyword in prompt_lower)
        complex_count = sum(1 for keyword in cls.COMPLEXITY_INDICATORS["complex"]
                           if keyword in prompt_lower)

        # Check for features and their weights
        for feature, weight in cls.FEATURE_WEIGHTS.items():
            if feature in prompt_lower:
                complexity_score += weight
                feature_count += 1

        # Analyze prompt structure
        sentences = prompt.split('.')
        word_count = len(prompt.split())
        feature_list_patterns = len(re.findall(r'[-•*]\s', prompt))

        # Calculate final complexity
        if simple_count > complex_count and complexity_score < 3:
            return "simple", 80
        elif complexity_score > 8 or complex_count > 2 or feature_count > 5:
            return "complex", 85
        elif word_count > 100 or feature_list_patterns > 3:
            return "complex", 75
        else:
            return "medium", 70

def display_welcome():
    """Display welcome message and tips"""
    print("🚀 " + "="*60)
    print("   CODER-BUDDY - AI Development Platform")
    print("   Powered by IONOS AI Model Hub")
    print("="*60)
    print("💡 Tips for best results:")
    print("  • Be specific about features you want")
    print("  • Mention design preferences (modern, minimal, etc.)")
    print("  • Specify technology if needed (React, vanilla JS)")
    print("  • Include responsive design requirements")
    print("  • List exact functionality needed")
    print()

def display_examples():
    """Show example prompts"""
    print("📝 Example prompts:")
    print()
    print("🟢 SIMPLE (Fast generation):")
    print("  'Create a landing page with hero section and contact info'")
    print("  'Build a simple calculator with basic operations'")
    print()
    print("🟡 MEDIUM (Balanced generation):")
    print("  'Create a todo app with add/edit/delete and local storage'")
    print("  'Build a portfolio site with projects gallery and contact form'")
    print()
    print("🔴 COMPLEX (Powerful models):")
    print("  'Create a blog platform with admin panel, CRUD operations, and search'")
    print("  'Build an e-commerce site with cart, checkout, and user accounts'")
    print()

def get_user_input() -> str:
    """Get project description from user with helpful prompts"""
    while True:
        print("📝 Describe your project (or 'examples' for inspiration, 'quit' to exit):")
        user_input = input("➤ ").strip()

        if not user_input:
            print("❌ Please enter a project description")
            continue

        if user_input.lower() == 'quit':
            sys.exit(0)

        if user_input.lower() == 'examples':
            display_examples()
            continue

        return user_input

def main():
    """Enhanced main function with intelligent model selection"""
    parser = argparse.ArgumentParser(description="Enhanced Coder-Buddy with Multi-Model Optimization")
    parser.add_argument("--recursion-limit", "-r", type=int, default=100,
                        help="Recursion limit for processing (default: 100)")
    parser.add_argument("--complexity", "-c", choices=["simple", "medium", "complex"],
                        help="Override automatic complexity detection")
    parser.add_argument("--models", "-m", action="store_true",
                        help="List available models and exit")
    parser.add_argument("--prompt", "-p", type=str,
                        help="Project prompt (skips interactive input)")

    args = parser.parse_args()

    # Show available models if requested
    if args.models:
        model_manager.list_available_models()
        return

    # Display welcome
    display_welcome()

    try:
        # Get user input
        if args.prompt:
            user_prompt = args.prompt
        else:
            user_prompt = get_user_input()

        # Analyze complexity
        if args.complexity:
            complexity = args.complexity
            confidence = 100
            print(f"🎛️ Manual complexity override: {complexity.upper()}")
        else:
            complexity, confidence = ProjectAnalyzer.analyze_complexity(user_prompt)
            print(f"🧠 Detected complexity: {complexity.upper()} (confidence: {confidence}%)")

        # Show what models will be used
        print(f"🤖 Models selected for {complexity} project:")
        if complexity == "simple":
            print("  • Planner: Meta-Llama-3.1-8B-Instruct (Fast)")
            print("  • Architect: Mistral-Nemo-Instruct-2407 (Balanced)")
            print("  • Coder: Meta-Llama-3.1-8B-Instruct (Fast)")
        elif complexity == "complex":
            print("  • Planner: Mistral-Nemo-Instruct-2407 (Balanced)")
            print("  • Architect: Meta-Llama-3.1-405B-Instruct-FP8 (Powerful)")
            print("  • Coder: Mistral-Nemo-Instruct-2407 (Balanced)")
        else:
            print("  • Planner: Mistral-Nemo-Instruct-2407 (Balanced)")
            print("  • Architect: Meta-Llama-3.1-405B-Instruct-FP8 (Powerful)")
            print("  • Coder: Meta-Llama-3.1-8B-Instruct (Fast)")

        print(f"\n🚀 Starting generation...")
        print(f"📝 Project: {user_prompt}")
        print("⏱️ Estimated time: " + {
            "simple": "2-5 minutes",
            "medium": "5-10 minutes",
            "complex": "10-20 minutes"
        }[complexity])
        print()

        # Run the agent
        result = agent.invoke(
            {"user_prompt": user_prompt},
            {"recursion_limit": args.recursion_limit}
        )

        print("🎉 Generation completed!")
        print("📁 Files created in: generated_project/")
        print("🌐 Open in browser: open generated_project/index.html")

        # Show file summary
        import os
        if os.path.exists("generated_project"):
            files = os.listdir("generated_project")
            print(f"📄 Generated {len(files)} files: {', '.join(files)}")

    except KeyboardInterrupt:
        print("\n⏹️ Generation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Try simplifying your request or check your IONOS token")
        sys.exit(1)

if __name__ == "__main__":
    main()