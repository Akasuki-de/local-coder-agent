# 🔍 Code Walkthrough: LangChain + LangGraph Implementation

## 📋 Table of Contents
1. [State Management](#state-management)
2. [Model Configuration](#model-configuration)
3. [Agent Implementation](#agent-implementation)
4. [Graph Construction](#graph-construction)
5. [Tool Integration](#tool-integration)
6. [Execution Flow](#execution-flow)

---

## 🔄 State Management

### LangGraph State Structure
```python
# The state is a simple dictionary that flows between nodes
# It accumulates data as it moves through the workflow

# Initial state (from user input)
state = {
    "user_prompt": "Create a todo app with dark mode"
}

# After Planner Agent
state = {
    "user_prompt": "Create a todo app with dark mode",
    "plan": Plan(
        name="Todo Application",
        description="A todo app with task management and dark mode",
        techstack="HTML, CSS, JavaScript",
        features=["Add tasks", "Delete tasks", "Dark mode toggle"],
        files=[
            File(path="index.html", purpose="Main HTML structure"),
            File(path="style.css", purpose="Styling and dark mode"),
            File(path="script.js", purpose="JavaScript functionality")
        ]
    )
}

# After Architect Agent
state = {
    "user_prompt": "...",
    "plan": Plan(...),
    "task_plan": TaskPlan(
        implementation_steps=[
            ImplementationTask(
                filepath="index.html",
                task_description="Create HTML structure with task input and list"
            ),
            ImplementationTask(
                filepath="style.css",
                task_description="Add CSS for layout and dark mode styles"
            ),
            # ... more tasks
        ]
    )
}
```

### Pydantic Models for Structure
```python
# agent/states.py - These models ensure consistent data structure
from pydantic import BaseModel
from typing import List

class File(BaseModel):
    path: str
    purpose: str

class Plan(BaseModel):
    name: str
    description: str
    techstack: str
    features: List[str]
    files: List[File]

class ImplementationTask(BaseModel):
    filepath: str
    task_description: str

class TaskPlan(BaseModel):
    implementation_steps: List[ImplementationTask]
    # model_config allows adding extra fields dynamically
    model_config = ConfigDict(extra="allow")
```

---

## 🤖 Model Configuration

### Multi-Model Setup
```python
# agent/multi_model_config.py
from langchain_openai import ChatOpenAI

# Different models for different task complexities
IONOS_MODELS = {
    ModelTier.FAST: {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "max_tokens": 4096,
        "temperature": 0.3  # Lower temperature for more focused output
    },
    ModelTier.BALANCED: {
        "model": "mistralai/Mistral-Nemo-Instruct-2407",
        "max_tokens": 8192,
        "temperature": 0.4
    },
    ModelTier.POWERFUL: {
        "model": "meta-llama/Meta-Llama-3.1-405B-Instruct-FP8",
        "max_tokens": 16384,
        "temperature": 0.2  # Very low for consistent, logical output
    }
}

class MultiModelManager:
    def get_model_for_task(self, task_type: TaskType, complexity: str) -> ChatOpenAI:
        """Returns optimized model based on task and complexity"""
        tier = self._determine_tier(task_type, complexity)
        config = IONOS_MODELS[tier]

        return ChatOpenAI(
            model=config["model"],
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_api_base=os.getenv("OPENAI_BASE_URL"),
            temperature=config["temperature"],
            max_tokens=config["max_tokens"]
        )
```

### Model Selection Logic
```python
# How the system chooses models for each agent
TASK_MODEL_MAPPING = {
    TaskType.PLANNING: ModelTier.BALANCED,     # Planning needs good reasoning
    TaskType.ARCHITECTURE: ModelTier.POWERFUL, # Architecture needs deep thinking
    TaskType.CODING: ModelTier.FAST,           # Coding can be fast for most tasks
}

# Complexity override logic
def get_model_for_task(self, task_type: TaskType, complexity: str = "medium"):
    base_tier = TASK_MODEL_MAPPING[task_type]

    if complexity == "simple" and base_tier != ModelTier.FAST:
        tier = ModelTier.FAST
    elif complexity == "complex":
        tier = ModelTier.POWERFUL
    else:
        tier = base_tier

    return self._get_or_create_model(tier)
```

---

## 🤖 Agent Implementation

### Planner Agent
```python
# agent/graph.py
def planner_agent(state: dict) -> dict:
    """Converts user prompt into structured Plan"""
    user_prompt = state["user_prompt"]
    print(f"🧠 Planner using: {planner_llm.model_name}")

    # Use structured output to ensure consistent format
    resp = planner_llm.with_structured_output(Plan).invoke(
        planner_prompt(user_prompt)
    )

    if resp is None:
        raise ValueError("Planner did not return a valid response.")

    # Return dictionary that gets merged into state
    return {"plan": resp}
```

### Structured Output Magic
```python
# The .with_structured_output() method does this:
# 1. Takes your Pydantic model (Plan)
# 2. Converts it to JSON schema
# 3. Instructs the LLM to output in that exact format
# 4. Validates and parses the response
# 5. Returns a proper Python object

# Instead of getting raw text like:
# "I'll create a todo app with HTML, CSS..."

# You get a structured Plan object:
Plan(
    name="Todo Application",
    description="...",
    # ... etc
)
```

### Architect Agent with Context
```python
def architect_agent(state: dict) -> dict:
    """Creates TaskPlan from Plan"""
    plan: Plan = state["plan"]  # Get plan from previous agent
    print(f"🏗️ Architect using: {architect_llm.model_name}")

    # Pass the plan as JSON to the prompt
    resp = architect_llm.with_structured_output(TaskPlan).invoke(
        architect_prompt(plan=plan.model_dump_json())
    )

    if resp is None:
        raise ValueError("Architect did not return a valid response.")

    # Add the original plan back to the response
    resp.plan = plan  # This works because of model_config extra="allow"

    return {"task_plan": resp}
```

---

## 🔄 Graph Construction

### LangGraph Setup
```python
# agent/graph.py
from langgraph.graph import StateGraph
from langgraph.constants import END

# Create state graph with dictionary state
graph = StateGraph(dict)

# Add nodes (each node is a function that takes state dict, returns state dict)
graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)

# Add edges (define the flow)
graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")

# Conditional edges (dynamic routing based on state)
graph.add_conditional_edges(
    "coder",
    # This function determines next node based on state
    lambda s: "END" if s.get("status") == "DONE" else "coder",
    # Mapping of conditions to nodes
    {"END": END, "coder": "coder"}
)

# Set entry point
graph.set_entry_point("planner")

# Compile into executable agent
agent = graph.compile()
```

### How Conditional Edges Work
```python
# The coder agent can loop back to itself or end
def coder_agent(state: dict) -> dict:
    coder_state: CoderState = state.get("coder_state")

    # Initialize if first run
    if coder_state is None:
        coder_state = CoderState(task_plan=state["task_plan"], current_step_idx=0)

    steps = coder_state.task_plan.implementation_steps

    # Check if we're done with all steps
    if coder_state.current_step_idx >= len(steps):
        return {"coder_state": coder_state, "status": "DONE"}  # This triggers END

    # Process current step
    current_task = steps[coder_state.current_step_idx]
    # ... process the task ...

    coder_state.current_step_idx += 1
    return {"coder_state": coder_state}  # This triggers loop back to "coder"
```

---

## 🛠️ Tool Integration

### LangChain Tools
```python
# agent/tools.py
from langchain_core.tools import tool

@tool
def write_file(path: str, content: str) -> str:
    """Write content to a file"""
    # Validation and safety checks
    if not _is_safe_path(path):
        raise ValueError(f"Unsafe path: {path}")

    # Ensure directory exists
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    # Write file
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return f"WROTE:{full_path}"

@tool
def read_file(path: str) -> str:
    """Read content from a file"""
    if not os.path.exists(full_path):
        return ""  # Return empty if file doesn't exist

    with open(full_path, 'r', encoding='utf-8') as f:
        return f.read()
```

### ReactAgent Integration
```python
# agent/graph.py
from langgraph.prebuilt import create_react_agent

def coder_agent(state: dict) -> dict:
    # ... setup code ...

    # Create agent with LLM and tools
    coder_tools = [read_file, write_file, list_files, get_current_directory]
    react_agent = create_react_agent(coder_llm, coder_tools)

    # The ReactAgent follows this pattern:
    # 1. Receive task description
    # 2. Reason about what needs to be done
    # 3. Decide which tools to use
    # 4. Execute tools
    # 5. Observe results
    # 6. Repeat until task complete

    system_prompt = coder_system_prompt()
    user_prompt = f"""
    Task: {current_task.task_description}
    File: {current_task.filepath}
    Existing content: {existing_content}
    Use write_file(path, content) to save your changes.
    """

    react_agent.invoke({
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    })
```

---

## ⚡ Execution Flow

### Complete Workflow
```python
# When you run: agent.invoke({"user_prompt": "Create a todo app"})

# 1. LangGraph initializes state
initial_state = {"user_prompt": "Create a todo app"}

# 2. Routes to planner node
state = planner_agent(initial_state)
# state = {"user_prompt": "...", "plan": Plan(...)}

# 3. Routes to architect node
state = architect_agent(state)
# state = {"user_prompt": "...", "plan": Plan(...), "task_plan": TaskPlan(...)}

# 4. Routes to coder node (first time)
state = coder_agent(state)
# state = {..., "coder_state": CoderState(current_step_idx=1)}

# 5. Conditional edge checks: status != "DONE", routes back to coder

# 6. Coder processes next task
state = coder_agent(state)
# state = {..., "coder_state": CoderState(current_step_idx=2)}

# 7. Loop continues until all tasks complete

# 8. Final coder call
state = coder_agent(state)
# state = {..., "coder_state": CoderState(...), "status": "DONE"}

# 9. Conditional edge routes to END
# Workflow complete!
```

### Error Handling & Validation
```python
# Throughout the workflow, several validation layers:

# 1. Pydantic model validation
try:
    plan = Plan(**response_data)
except ValidationError as e:
    raise ValueError(f"Invalid plan structure: {e}")

# 2. LLM response validation
if resp is None:
    raise ValueError("Agent did not return a valid response.")

# 3. File safety validation
def _is_safe_path(path: str) -> bool:
    """Ensure files are only written to safe locations"""
    safe_dir = os.path.abspath("generated_project")
    target_path = os.path.abspath(os.path.join(safe_dir, path))
    return target_path.startswith(safe_dir)

# 4. Tool execution validation
@tool
def write_file(path: str, content: str) -> str:
    if not _is_safe_path(path):
        raise ValueError(f"Attempt to write outside project root: {path}")
```

This architecture creates a robust, maintainable system that leverages the best of LangChain's tools and LangGraph's orchestration capabilities! 🚀