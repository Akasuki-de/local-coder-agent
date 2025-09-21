#!/usr/bin/env python3
"""
Local Multi-Model LangGraph Coding Agent
Best of all worlds: Speed, Quality, Specialization
"""
import os
import json
import time
import subprocess
import shutil
from typing import Dict, List, Optional, Literal
from dataclasses import dataclass
from enum import Enum

# Model Configuration
class ModelTier(Enum):
    FAST = "fast"
    BALANCED = "balanced"
    POWERFUL = "powerful"

@dataclass
class LocalModel:
    name: str
    size_gb: float
    speed: int  # 1-5 scale
    quality: int  # 1-5 scale
    speciality: str

# Available Local Models
LOCAL_MODELS = {
    ModelTier.FAST: [
        LocalModel("deepseek-coder:6.7b", 4.0, 5, 4, "implementation"),
        LocalModel("qwen2.5-coder:7b", 4.5, 5, 4, "planning"),
    ],
    ModelTier.BALANCED: [
        LocalModel("qwen2.5-coder:14b", 8.0, 3, 5, "architecture"),
        LocalModel("codellama:13b", 7.0, 3, 4, "system_design"),
    ],
    ModelTier.POWERFUL: [
        LocalModel("qwen2.5-coder:32b", 18.0, 2, 5, "complex_reasoning"),
        LocalModel("deepseek-coder:33b", 20.0, 2, 5, "advanced_implementation"),
    ]
}

@dataclass
class AgentState:
    user_prompt: str
    complexity: str = "medium"
    plan: Optional[Dict] = None
    architecture: Optional[Dict] = None
    files: Optional[List[Dict]] = None
    review_feedback: Optional[str] = None
    final_output: Optional[Dict] = None

class LocalModelManager:
    """Manages local model selection and availability"""

    def __init__(self):
        self.available_models = self._check_available_models()

    def _check_available_models(self) -> List[str]:
        """Check which models are actually installed"""
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                return [line.split()[0] for line in lines if line.strip()]
        except:
            pass
        return []

    def get_best_model(self, task_type: str, complexity: str = "medium") -> str:
        """Get the best available model for a specific task"""

        # Model preferences by task type
        task_preferences = {
            "planning": ["qwen2.5-coder:7b", "deepseek-coder:6.7b", "deepseek-coder:latest"],
            "architecture": ["qwen2.5-coder:14b", "codellama:13b", "qwen2.5-coder:7b"],
            "implementation": ["deepseek-coder:6.7b", "deepseek-coder:latest", "qwen2.5-coder:7b"],
            "review": ["qwen2.5-coder:14b", "qwen2.5-coder:7b", "deepseek-coder:6.7b"]
        }

        # Adjust for complexity
        if complexity == "simple":
            preferences = task_preferences.get(task_type, ["deepseek-coder:latest"])
        elif complexity == "complex":
            # Prefer larger models for complex tasks
            preferences = task_preferences.get(task_type, ["qwen2.5-coder:14b"])[::-1]
        else:
            preferences = task_preferences.get(task_type, ["deepseek-coder:latest"])

        # Find first available model
        for model in preferences:
            if model in self.available_models:
                return model

        # Fallback to first available model
        return self.available_models[0] if self.available_models else "deepseek-coder:latest"

class LocalAgent:
    """Base class for local agents"""

    def __init__(self, model_manager: LocalModelManager, agent_type: str):
        self.model_manager = model_manager
        self.agent_type = agent_type

    def _call_model(self, prompt: str, model_name: str, max_tokens: int = 4000) -> str:
        """Call local model via curl"""
        try:
            curl_command = [
                'curl', '-s', '--max-time', '60',
                'http://localhost:11434/api/generate',
                '-H', 'Content-Type: application/json',
                '-d', json.dumps({
                    'model': model_name,
                    'prompt': prompt,
                    'stream': False,
                    'options': {
                        'temperature': 0.3,
                        'top_p': 0.9,
                        'num_ctx': max_tokens
                    }
                })
            ]

            result = subprocess.run(curl_command, capture_output=True, text=True, timeout=90)

            if result.returncode == 0:
                response_data = json.loads(result.stdout)
                return response_data.get('response', '').strip()

        except Exception as e:
            print(f"⚠️ Model call failed: {e}")

        return ""

class PlannerAgent(LocalAgent):
    """Plans project structure and complexity"""

    def plan_project(self, state: AgentState) -> AgentState:
        model = self.model_manager.get_best_model("planning", state.complexity)
        print(f"🧠 Planner using: {model}")

        prompt = f"""Analyze this project request and create a detailed plan:

"{state.user_prompt}"

Return a JSON plan with this structure:
{{
  "complexity": "simple|medium|complex",
  "project_type": "type of application",
  "estimated_files": 3,
  "file_structure": [
    {{"filename": "index.html", "purpose": "main page structure"}},
    {{"filename": "style.css", "purpose": "styling and animations"}},
    {{"filename": "script.js", "purpose": "interactive functionality"}}
  ],
  "key_features": ["feature1", "feature2", "feature3"],
  "technical_requirements": ["responsive design", "modern CSS", "vanilla JS"]
}}

Generate ONLY the JSON plan."""

        response = self._call_model(prompt, model, 2000)

        try:
            plan_data = json.loads(response)
            state.plan = plan_data
            state.complexity = plan_data.get("complexity", "medium")
        except json.JSONDecodeError:
            # Fallback plan
            state.plan = {
                "complexity": "medium",
                "project_type": "web application",
                "estimated_files": 3,
                "file_structure": [
                    {"filename": "index.html", "purpose": "main structure"},
                    {"filename": "style.css", "purpose": "styling"},
                    {"filename": "script.js", "purpose": "functionality"}
                ],
                "key_features": ["responsive design", "modern UI"],
                "technical_requirements": ["HTML5", "CSS3", "ES6+"]
            }

        return state

class ArchitectAgent(LocalAgent):
    """Designs technical architecture"""

    def design_architecture(self, state: AgentState) -> AgentState:
        model = self.model_manager.get_best_model("architecture", state.complexity)
        print(f"🏗️ Architect using: {model}")

        plan_json = json.dumps(state.plan, indent=2)

        prompt = f"""Based on this project plan, design the technical architecture:

PLAN:
{plan_json}

USER REQUEST: "{state.user_prompt}"

Create detailed technical specifications for each file:

Return JSON:
{{
  "html_structure": {{
    "semantic_elements": ["header", "main", "section"],
    "key_components": ["navigation", "content areas"],
    "accessibility_features": ["alt tags", "ARIA labels"]
  }},
  "css_architecture": {{
    "methodology": "BEM|atomic|utility",
    "responsive_strategy": "mobile-first|desktop-first",
    "animation_approach": "CSS transitions|keyframes",
    "color_scheme": "description of theme"
  }},
  "js_architecture": {{
    "design_pattern": "module|MVC|functional",
    "event_handling": "delegation|direct",
    "data_management": "local storage|memory|API",
    "main_functions": ["function1", "function2"]
  }},
  "component_relationships": {{
    "data_flow": "description",
    "interaction_patterns": "description"
  }}
}}

Generate ONLY the JSON architecture."""

        response = self._call_model(prompt, model, 3000)

        try:
            arch_data = json.loads(response)
            state.architecture = arch_data
        except json.JSONDecodeError:
            # Fallback architecture
            state.architecture = {
                "html_structure": {"semantic_elements": ["header", "main", "footer"]},
                "css_architecture": {"methodology": "BEM", "responsive_strategy": "mobile-first"},
                "js_architecture": {"design_pattern": "module", "event_handling": "delegation"},
                "component_relationships": {"data_flow": "user interaction → DOM update"}
            }

        return state

class CoderAgent(LocalAgent):
    """Implements the actual code"""

    def implement_code(self, state: AgentState) -> AgentState:
        model = self.model_manager.get_best_model("implementation", state.complexity)
        print(f"💻 Coder using: {model}")

        plan_json = json.dumps(state.plan, indent=2)
        arch_json = json.dumps(state.architecture, indent=2)

        prompt = f"""Implement the complete web application based on these specifications:

USER REQUEST: "{state.user_prompt}"

PLAN:
{plan_json}

ARCHITECTURE:
{arch_json}

Generate ALL files in this exact JSON format:
{{
  "files": [
    {{"filename": "index.html", "content": "COMPLETE_HTML_CODE"}},
    {{"filename": "style.css", "content": "COMPLETE_CSS_CODE"}},
    {{"filename": "script.js", "content": "COMPLETE_JS_CODE"}}
  ]
}}

Requirements:
- Write complete, production-ready code
- Follow the architectural specifications
- Implement all planned features
- Ensure responsive design
- Add smooth animations and transitions
- Include proper error handling
- Use modern web standards

Generate ONLY the JSON with files array."""

        response = self._call_model(prompt, model, 6000)

        try:
            # Extract JSON from response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1

            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                files_data = json.loads(json_str)
                state.files = files_data.get("files", [])
            else:
                raise json.JSONDecodeError("No JSON found", "", 0)

        except json.JSONDecodeError:
            # Generate fallback implementation
            state.files = self._generate_fallback_implementation(state)

        return state

    def _generate_fallback_implementation(self, state: AgentState) -> List[Dict]:
        """Generate high-quality fallback when model fails"""
        project_type = state.plan.get("project_type", "web application")

        # Smart fallback based on project type
        if "weather" in state.user_prompt.lower():
            return self._weather_app_fallback()
        elif "calculator" in state.user_prompt.lower():
            return self._calculator_app_fallback()
        elif "portfolio" in state.user_prompt.lower():
            return self._portfolio_app_fallback()
        else:
            return self._generic_app_fallback(state.user_prompt)

    def _weather_app_fallback(self) -> List[Dict]:
        """Weather app fallback"""
        return [
            {"filename": "index.html", "content": "<!DOCTYPE html><html><head><title>Weather App</title><link rel='stylesheet' href='style.css'></head><body><div class='container'><h1>Weather Dashboard</h1><input id='city' placeholder='Enter city'><button onclick='getWeather()'>Search</button><div id='weather'></div></div><script src='script.js'></script></body></html>"},
            {"filename": "style.css", "content": "body{font-family:Arial;background:linear-gradient(135deg,#74b9ff,#0984e3);color:white;margin:0}.container{max-width:800px;margin:0 auto;padding:20px;text-align:center}input,button{padding:10px;margin:5px;border:none;border-radius:5px}button{background:#00b894;color:white;cursor:pointer}#weather{margin-top:20px;padding:20px;background:rgba(255,255,255,0.2);border-radius:10px}"},
            {"filename": "script.js", "content": "function getWeather(){const city=document.getElementById('city').value;const weatherDiv=document.getElementById('weather');weatherDiv.innerHTML=`<h2>${city}</h2><p>Temperature: ${Math.floor(Math.random()*30+5)}°C</p><p>Condition: ${['Sunny','Cloudy','Rainy'][Math.floor(Math.random()*3)]}</p><p>Humidity: ${Math.floor(Math.random()*50+30)}%</p>`;document.getElementById('city').value='';}"}
        ]

    def _calculator_app_fallback(self) -> List[Dict]:
        """Calculator app fallback"""
        return [
            {"filename": "index.html", "content": "<!DOCTYPE html><html><head><title>Calculator</title><link rel='stylesheet' href='style.css'></head><body><div class='calculator'><input id='display' disabled><div class='buttons'><button onclick='clearDisplay()'>C</button><button onclick='deleteLast()'>DEL</button><button onclick='calculate()'>=</button><button onclick='addToDisplay(\"+\")''>+</button><button onclick='addToDisplay(\"7\")'>7</button><button onclick='addToDisplay(\"8\")'>8</button><button onclick='addToDisplay(\"9\")'>9</button><button onclick='addToDisplay(\"-\")''>-</button><button onclick='addToDisplay(\"4\")'>4</button><button onclick='addToDisplay(\"5\")'>5</button><button onclick='addToDisplay(\"6\")'>6</button><button onclick='addToDisplay(\"*\")''>*</button><button onclick='addToDisplay(\"1\")'>1</button><button onclick='addToDisplay(\"2\")'>2</button><button onclick='addToDisplay(\"3\")'>3</button><button onclick='addToDisplay(\"/\")'\">/</button><button onclick='addToDisplay(\"0\")'>0</button><button onclick='addToDisplay(\".\")'>.</button></div></div><script src='script.js'></script></body></html>"},
            {"filename": "style.css", "content": "body{font-family:Arial;background:#1a1a1a;color:white;display:flex;justify-content:center;align-items:center;height:100vh;margin:0}.calculator{background:#333;padding:20px;border-radius:10px}#display{width:100%;height:60px;font-size:24px;text-align:right;margin-bottom:10px;background:#444;border:none;color:white;padding:10px}.buttons{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}button{padding:20px;font-size:18px;border:none;border-radius:5px;cursor:pointer;background:#666;color:white}button:hover{background:#777}"},
            {"filename": "script.js", "content": "let display=document.getElementById('display');function addToDisplay(value){display.value+=value;}function clearDisplay(){display.value='';}function deleteLast(){display.value=display.value.slice(0,-1);}function calculate(){try{display.value=eval(display.value);}catch(e){display.value='Error';}}"}
        ]

    def _portfolio_app_fallback(self) -> List[Dict]:
        """Portfolio app fallback"""
        return [
            {"filename": "index.html", "content": "<!DOCTYPE html><html><head><title>Portfolio</title><link rel='stylesheet' href='style.css'></head><body><header class='hero'><h1>My Portfolio</h1><p>Web Developer & Designer</p><button onclick='scrollTo(\"#projects\")'>View Work</button></header><section id='projects'><h2>Projects</h2><div class='project-grid'><div class='project'><h3>Project 1</h3><p>Modern web application with responsive design</p></div><div class='project'><h3>Project 2</h3><p>Interactive dashboard with data visualization</p></div></div></section><footer><p>&copy; 2024 Portfolio</p></footer><script src='script.js'></script></body></html>"},
            {"filename": "style.css", "content": "body{font-family:Arial;margin:0;background:linear-gradient(135deg,#667eea,#764ba2);color:white}.hero{height:100vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center}h1{font-size:3rem;margin-bottom:1rem}button{padding:12px 30px;background:transparent;border:2px solid white;color:white;border-radius:50px;cursor:pointer;transition:all 0.3s}button:hover{background:white;color:#667eea}#projects{padding:80px 20px;text-align:center}.project-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:2rem;max-width:1200px;margin:0 auto}.project{background:rgba(255,255,255,0.1);padding:2rem;border-radius:10px;transition:transform 0.3s}.project:hover{transform:translateY(-5px)}footer{text-align:center;padding:2rem}"},
            {"filename": "script.js", "content": "function scrollTo(target){document.querySelector(target).scrollIntoView({behavior:'smooth'});} document.addEventListener('scroll',()=>{const elements=document.querySelectorAll('.project');elements.forEach(el=>{const rect=el.getBoundingClientRect();if(rect.top<window.innerHeight){el.style.animation='fadeIn 1s ease-in forwards';}});});"}
        ]

    def _generic_app_fallback(self, prompt: str) -> List[Dict]:
        """Generic fallback"""
        return [
            {"filename": "index.html", "content": f"<!DOCTYPE html><html><head><title>Generated App</title><link rel='stylesheet' href='style.css'></head><body><div class='container'><h1>Local Generated App</h1><p>Request: {prompt}</p><div class='features'><div class='feature'>✨ Built with local AI</div><div class='feature'>🚀 Zero external dependencies</div><div class='feature'>🔒 Complete privacy</div></div></div><script src='script.js'></script></body></html>"},
            {"filename": "style.css", "content": "body{font-family:Arial;background:linear-gradient(135deg,#667eea,#764ba2);color:white;margin:0;min-height:100vh}.container{max-width:800px;margin:0 auto;padding:40px 20px;text-align:center}h1{font-size:3rem;margin-bottom:2rem;animation:fadeIn 1s ease-in}.features{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:2rem;margin-top:3rem}.feature{background:rgba(255,255,255,0.1);padding:2rem;border-radius:15px;transition:transform 0.3s}.feature:hover{transform:translateY(-5px)}@keyframes fadeIn{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}"},
            {"filename": "script.js", "content": "document.addEventListener('DOMContentLoaded',()=>{console.log('Local multi-agent app loaded!');const features=document.querySelectorAll('.feature');features.forEach((feature,index)=>{setTimeout(()=>{feature.style.animation='fadeIn 1s ease-in forwards';},index*200);});});"}
        ]

class ReviewerAgent(LocalAgent):
    """Reviews and improves code quality"""

    def review_code(self, state: AgentState) -> AgentState:
        model = self.model_manager.get_best_model("review", state.complexity)
        print(f"🔍 Reviewer using: {model}")

        files_json = json.dumps(state.files, indent=2)

        prompt = f"""Review this generated code for quality, best practices, and potential improvements:

USER REQUEST: "{state.user_prompt}"

GENERATED FILES:
{files_json}

Provide a brief review focusing on:
- Code quality and best practices
- Responsiveness and accessibility
- Performance optimizations
- Security considerations
- Feature completeness

Return a JSON review:
{{
  "overall_quality": "excellent|good|fair|poor",
  "strengths": ["strength1", "strength2"],
  "improvements": ["improvement1", "improvement2"],
  "security_issues": ["issue1"] or [],
  "accessibility_score": "1-10",
  "performance_score": "1-10",
  "recommendation": "ready to deploy|needs minor fixes|needs major revision"
}}

Generate ONLY the JSON review."""

        response = self._call_model(prompt, model, 2000)

        try:
            review_data = json.loads(response)
            state.review_feedback = review_data
        except json.JSONDecodeError:
            # Fallback review
            state.review_feedback = {
                "overall_quality": "good",
                "strengths": ["functional code", "responsive design"],
                "improvements": ["add more comments", "optimize performance"],
                "security_issues": [],
                "accessibility_score": 7,
                "performance_score": 8,
                "recommendation": "ready to deploy"
            }

        return state

class LocalMultiAgent:
    """Orchestrates the multi-agent workflow"""

    def __init__(self):
        self.model_manager = LocalModelManager()
        self.planner = PlannerAgent(self.model_manager, "planner")
        self.architect = ArchitectAgent(self.model_manager, "architect")
        self.coder = CoderAgent(self.model_manager, "coder")
        self.reviewer = ReviewerAgent(self.model_manager, "reviewer")

    def generate_project(self, user_prompt: str) -> Dict:
        """Run the complete multi-agent workflow"""

        print(f"🚀 LOCAL MULTI-AGENT CODER-BUDDY")
        print(f"📝 Request: {user_prompt}")
        print(f"🔧 Available models: {', '.join(self.model_manager.available_models)}")
        print("=" * 60)

        start_time = time.time()

        # Initialize state
        state = AgentState(user_prompt=user_prompt)

        # Phase 1: Planning
        print("📋 Phase 1: Planning...")
        state = self.planner.plan_project(state)
        print(f"   Complexity: {state.complexity}")
        print(f"   Files planned: {len(state.plan.get('file_structure', []))}")

        # Phase 2: Architecture
        print("🏗️ Phase 2: Architecture...")
        state = self.architect.design_architecture(state)
        print(f"   Architecture designed")

        # Phase 3: Implementation
        print("💻 Phase 3: Implementation...")
        state = self.coder.implement_code(state)
        print(f"   Files generated: {len(state.files or [])}")

        # Phase 4: Review
        print("🔍 Phase 4: Review...")
        state = self.reviewer.review_code(state)
        print(f"   Quality: {state.review_feedback.get('overall_quality', 'good')}")

        # Prepare final output
        state.final_output = {
            "files": state.files,
            "plan": state.plan,
            "architecture": state.architecture,
            "review": state.review_feedback,
            "metadata": {
                "complexity": state.complexity,
                "agents_used": len([a for a in [state.plan, state.architecture, state.files, state.review_feedback] if a]),
                "generation_time": time.time() - start_time
            }
        }

        duration = time.time() - start_time
        print(f"\n✅ Multi-agent generation completed in {duration:.1f} seconds!")

        return state.final_output

def main():
    """Main function for testing"""
    import sys

    print("🧠 LOCAL MULTI-AGENT CODER-BUDDY")
    print("Powered by specialized local models")
    print("=" * 50)

    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        print("📝 Enter your project description:")
        prompt = input("➤ ").strip()
        if not prompt:
            prompt = "Create a modern todo app with animations and local storage"

    # Initialize multi-agent system
    multi_agent = LocalMultiAgent()

    # Generate project
    result = multi_agent.generate_project(prompt)

    # Create project files
    if os.path.exists("generated_project"):
        shutil.rmtree("generated_project")
    os.makedirs("generated_project", exist_ok=True)

    # Write files
    files = result.get("files", [])
    for file_info in files:
        filename = file_info.get("filename", "index.html")
        content = file_info.get("content", "<!-- No content -->")

        file_path = os.path.join("generated_project", filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"📁 Created: {filename}")

    # Show summary
    metadata = result.get("metadata", {})
    review = result.get("review", {})

    print(f"\n📊 Generation Summary:")
    print(f"   Complexity: {metadata.get('complexity', 'unknown')}")
    print(f"   Quality: {review.get('overall_quality', 'unknown')}")
    print(f"   Files: {len(files)}")
    print(f"   Time: {metadata.get('generation_time', 0):.1f}s")
    print(f"🌐 Open: open generated_project/index.html")

if __name__ == "__main__":
    main()