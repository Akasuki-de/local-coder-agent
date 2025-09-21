"""
Fast version of the graph using only the 8B model for quick testing
"""
import os
from dotenv import load_dotenv
from langchain.globals import set_verbose, set_debug
from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.prebuilt import create_react_agent

from fast_config import get_fast_llm
from agent.prompts import *
from agent.states import *
from agent.tools import write_file, read_file, get_current_directory, list_files

_ = load_dotenv()

# Disable verbose logging for speed
set_debug(False)
set_verbose(False)

# Use fast model for all agents
fast_llm = get_fast_llm()

def planner_agent_fast(state: dict) -> dict:
    """Fast planner using 8B model only"""
    user_prompt = state["user_prompt"]
    print(f"⚡ Fast Planner using: {fast_llm.model_name}")

    resp = fast_llm.with_structured_output(Plan).invoke(
        planner_prompt(user_prompt)
    )
    if resp is None:
        raise ValueError("Planner did not return a valid response.")
    return {"plan": resp}

def architect_agent_fast(state: dict) -> dict:
    """Fast architect using 8B model only"""
    plan: Plan = state["plan"]
    print(f"⚡ Fast Architect using: {fast_llm.model_name}")

    resp = fast_llm.with_structured_output(TaskPlan).invoke(
        architect_prompt(plan=plan.model_dump_json())
    )
    if resp is None:
        raise ValueError("Architect did not return a valid response.")

    resp.plan = plan
    return {"task_plan": resp}

def coder_agent_fast(state: dict) -> dict:
    """Fast coder using 8B model only"""
    coder_state: CoderState = state.get("coder_state")
    if coder_state is None:
        coder_state = CoderState(task_plan=state["task_plan"], current_step_idx=0)

    steps = coder_state.task_plan.implementation_steps
    if coder_state.current_step_idx >= len(steps):
        return {"coder_state": coder_state, "status": "DONE"}

    current_task = steps[coder_state.current_step_idx]
    existing_content = read_file.run(current_task.filepath)

    system_prompt = coder_system_prompt()
    user_prompt = (
        f"Task: {current_task.task_description}\n"
        f"File: {current_task.filepath}\n"
        f"Existing content:\n{existing_content}\n"
        "Use write_file(path, content) to save your changes."
    )

    coder_tools = [read_file, write_file, list_files, get_current_directory]
    react_agent = create_react_agent(fast_llm, coder_tools)
    print(f"⚡ Fast Coder using: {fast_llm.model_name}")

    react_agent.invoke({"messages": [{"role": "system", "content": system_prompt},
                                     {"role": "user", "content": user_prompt}]})

    coder_state.current_step_idx += 1
    return {"coder_state": coder_state}

# Create fast graph
fast_graph = StateGraph(dict)

fast_graph.add_node("planner", planner_agent_fast)
fast_graph.add_node("architect", architect_agent_fast)
fast_graph.add_node("coder", coder_agent_fast)

fast_graph.add_edge("planner", "architect")
fast_graph.add_edge("architect", "coder")
fast_graph.add_conditional_edges(
    "coder",
    lambda s: "END" if s.get("status") == "DONE" else "coder",
    {"END": END, "coder": "coder"}
)

fast_graph.set_entry_point("planner")
fast_agent = fast_graph.compile()

if __name__ == "__main__":
    # Quick test
    result = fast_agent.invoke(
        {"user_prompt": "Create a simple HTML page that says Hello World in red text"},
        {"recursion_limit": 10}
    )
    print("✅ Fast test completed!")